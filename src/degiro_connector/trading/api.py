import logging
import pkgutil
from pathlib import Path
from typing import Any, Callable, Iterable

from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.core.constants import urls
from degiro_connector.core.exceptions import ActionDisabledError
from degiro_connector.core.helpers.lazy_loader import InitArgs, LazyLoader, Pair
from degiro_connector.core.models.model_connection import ModelConnection
from degiro_connector.core.models.model_session import BlockedRequest, ModelSession
from degiro_connector.trading.models.credentials import Credentials

# Actions which place, change or cancel orders, or modify the account (notes, favourites).
# `check_order` is not part of it: it only validates an order and returns its fees.
SENSITIVE_ACTIONS = frozenset(
    {
        "confirm_order",
        "update_order",
        "delete_order",
        "create_favorite",
        "delete_favorite",
        "delete_favorite_product",
        "move_favorite",
        "put_favorite_product",
        "rename_favorite",
        "create_note",
        "delete_note",
        "edit_note",
    }
)

WRITE_METHODS = frozenset({"POST", "PUT", "DELETE", "PATCH"})

# Same protection at the HTTP level, so a disabled action can't be reached another way.
BLOCKED_REQUESTS: dict[str, BlockedRequest] = {
    "check_order": (frozenset({"POST"}), urls.ORDER_CHECK),
    # these three share one URL and differ by method
    "confirm_order": (frozenset({"POST"}), urls.ORDER_CONFIRM),
    "update_order": (frozenset({"PUT"}), urls.ORDER_UPDATE),
    "delete_order": (frozenset({"DELETE"}), urls.ORDER_DELETE),
    "favorites": (WRITE_METHODS, urls.FAVOURITES_LIST),
    "notes": (WRITE_METHODS, urls.NOTES_LIST),
}


def _blocked_requests(disabled_actions: frozenset[str]) -> list[BlockedRequest]:
    blocked = []
    for action in disabled_actions:
        if action in BLOCKED_REQUESTS:
            blocked.append(BLOCKED_REQUESTS[action])
        elif "favorite" in action:
            blocked.append(BLOCKED_REQUESTS["favorites"])
        elif "note" in action:
            blocked.append(BLOCKED_REQUESTS["notes"])
    return list(dict.fromkeys(blocked))


class API:
    TRADING_TIMEOUT = 1800
    PKG_PATH = "degiro_connector.trading.actions"
    CLS_PREFIX = "Action"
    MOD_PREFIX = "action_"
    ROOT_PATH = Path(__file__).absolute().parent.parent.parent.resolve()

    @classmethod
    def build_action_list(cls) -> list[str]:
        # SETUP PATH
        path = cls.PKG_PATH
        path = str(Path(cls.ROOT_PATH, *path.split(".")).resolve())

        # BUILD MODULE LIST
        action_list = list()
        for module in pkgutil.iter_modules([path]):
            if (
                not module.ispkg
                and module.name[: len(cls.MOD_PREFIX)] == cls.MOD_PREFIX
            ):
                action_list.append(module.name[len(cls.MOD_PREFIX) :])

        return action_list

    @property
    def action_list(self) -> list[str]:
        return self._action_list

    @property
    def disabled_actions(self) -> frozenset[str]:
        return self._disabled_actions

    @property
    def connection_storage(self) -> ModelConnection:
        return self._connection_storage

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    @property
    def session_storage(self) -> ModelSession:
        return self._session_storage

    def load(
        self,
        action: str,
        init_args: InitArgs | None = None,
    ) -> object | None:
        logger = self._logger
        action_list = self._action_list

        if action in self._disabled_actions:
            raise ActionDisabledError(f"Action disabled: {action}")

        if action not in action_list:
            logger.info("Not in action_list")
            logger.info("action : %s", action)
            logger.info("action_list : %s", action_list)
            return None

        # SETUP CLASS NAME
        cap_words_action = action.replace("_", " ").title().replace(" ", "")
        class_name = self.CLS_PREFIX + cap_words_action

        # SETUP PATHS
        module_path = self.PKG_PATH + "." + self.MOD_PREFIX + action

        # SETUP PAIR
        pair = Pair(
            module_path=module_path,
            class_name=class_name,
        )

        return LazyLoader.load_pair(pair=pair, init_args=init_args)

    def __init__(
        self,
        credentials: Credentials,
        connection_storage: ModelConnection | None = None,
        logger: logging.Logger | None = None,
        preload: bool = True,
        session_storage: ModelSession | None = None,
        read_only: bool = False,
        disabled_actions: Iterable[str] | None = None,
    ):
        """
        Args:
            read_only (bool, optional):
                Disables every action in `SENSITIVE_ACTIONS`: placing, changing or cancelling
                orders and modifying notes or favourites. Defaults to False.
            disabled_actions (Iterable[str], optional):
                Further actions to disable, e.g. {"check_order"}. Defaults to None.

        Disabled actions raise `ActionDisabledError`, and their HTTP requests are refused by the
        session before being sent.
        """
        all_actions = self.build_action_list()
        disabled = frozenset(disabled_actions or ())
        if read_only:
            disabled |= SENSITIVE_ACTIONS
        unknown = disabled - set(all_actions)
        if unknown:
            raise ValueError(f"Unknown actions: {sorted(unknown)}")
        self._disabled_actions = disabled

        self._credentials = credentials
        self._connection_storage = connection_storage or ModelConnection(
            timeout=self.TRADING_TIMEOUT,
        )
        self._logger = logger or logging.getLogger(self.__module__)
        blocked_requests = _blocked_requests(disabled)
        if session_storage is not None and blocked_requests:
            raise ValueError(
                "Pass either `session_storage` or disabled actions, not both."
            )
        self._session_storage = session_storage or ModelSession(
            hooks=self._connection_storage.build_hooks(),
            blocked_requests=blocked_requests,
        )
        self._action_list = [a for a in all_actions if a not in disabled]

        if preload:
            self.setup_all_actions()

    def setup_all_actions(self):
        action_list = self._action_list
        for action in action_list:
            self.setup_one_action(action=action)

    def setup_one_action(self, action: str):
        logger = self._logger
        init_args = InitArgs(
            credentials=self._credentials,
            connection_storage=self._connection_storage,
            session_storage=self._session_storage,
        )
        action_instance = self.load(
            action=action,
            init_args=init_args,
        )
        if not isinstance(action_instance, AbstractAction):
            raise TypeError(
                "Not a `AbstractAction` : %s / %s " % (action, action_instance)
            )

        logger.debug("setup_one_action : %s", action)
        setattr(self, action, action_instance)

    def __getattr__(self, item) -> Callable[..., Any]:
        logger = self._logger
        logger.debug("CALLING __GETATTR__, on item : %s", item)
        if item in self.__dict__.get("_disabled_actions", ()):
            raise ActionDisabledError(f"Action disabled: {item}")

        if item in self._action_list:
            action = item
            self.setup_one_action(action=action)

            return getattr(self, action)

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )
