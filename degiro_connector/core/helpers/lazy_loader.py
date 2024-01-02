import abc
import importlib
import importlib.util
from types import ModuleType
from typing import Optional

# IMPORTATION THIRDPARTY


"""
What to load ?
- Quotecast : Actions
    degiro_connector/quotecast/actions/<action>/action_<action>.py

- Trading : Actions
    degiro_connector/trading/actions/<action>/action_<action>.py

"""


class Pair:
    @property
    def module_path(self) -> str:
        return self._module_path

    @property
    def class_name(self) -> str:
        return self._class_name

    def __init__(self, module_path: str, class_name: str):
        self._module_path = module_path
        self._class_name = class_name


class InitArgs:
    @property
    def args(self) -> list:
        return self._args

    @property
    def kwargs(self) -> dict:
        return self._kwargs

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs


class LazyLoader(abc.ABC):
    @staticmethod
    def load_instance(
        module: Optional[ModuleType],
        class_name: str,
        init_args: InitArgs = None,
    ) -> Optional[object]:
        """Load an instance of a class if possible.

        Args:
            module (ModuleType): [description]
            class_name (str): [description]

        Returns:
            object: [description]
        """

        instance = None
        if (
            module is not None
            and isinstance(module, ModuleType)
            and hasattr(module, class_name)
        ):
            init_args = init_args or InitArgs()
            args = init_args.args
            kwargs = init_args.kwargs
            instance = getattr(module, class_name)(*args, **kwargs)

        return instance

    @staticmethod
    def load_module(module_path: str) -> Optional[ModuleType]:
        """Load a module from a path.

        Args:
            module_path (str):
                Module"s path.

        Returns:
            Optional[ModuleType]:
                Loaded module or None.
        """

        try:
            spec = importlib.util.find_spec(module_path)
        except ModuleNotFoundError:
            spec = None

        if spec is None:
            return None
        else:
            # module = importlib.util.module_from_spec(spec)
            # sys.modules[module_path] = module
            # spec.loader.exec_module(module)
            module = importlib.import_module(module_path)

            return module

    @classmethod
    def load_pair(
        cls,
        pair: Pair,
        init_args: InitArgs = None,
    ) -> Optional[object]:
        module = cls.load_module(module_path=pair.module_path)
        instance = cls.load_instance(
            module=module,
            class_name=pair.class_name,
            init_args=init_args,
        )

        return instance

    @classmethod
    def load_module_list(
        cls,
        module_path_list: list[str],
    ) -> Optional[object]:
        """Load the first valid module among a `module_path_list`.

        Args:
            module_path_list (list[str]):
                list of `[module_path, class_name]` pair.

        Returns:
            Optional[ModuleType]:
                Loaded module or None.
        """

        module = None
        for module_path in module_path_list:
            module = cls.load_module(module_path=module_path)
            if module is not None:
                break

        return module

    @classmethod
    def load_pair_list(
        cls,
        pair_list: list[Pair],
        init_args: InitArgs = None,
    ) -> Optional[object]:
        """Load the first valid instance among a `pair_list`.

        Args:
            pairs (list[Pair]):
                list of Pair.

        Returns:
            Optional[ModuleType]:
                Loaded instance or None.
        """

        instance = None
        for pair in pair_list:
            instance = cls.load_pair(pair=pair, init_args=init_args)
            if instance is not None:
                break

        return instance
