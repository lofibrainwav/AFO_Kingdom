from typing import Any, Iterator, Tuple

class Module:
    def named_modules(self) -> Iterator[Tuple[str, "Module"]]: ...
    def parameters(self) -> Iterator[Any]: ...

class Linear(Module):
    weight: Any
    bias: Any
    input_dims: int
    output_dims: int
    quantization_info: Any
    dwq_info: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
