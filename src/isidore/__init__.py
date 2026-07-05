"""isidore — compile an agent-oriented wiki from your codebase's structure graph.

Named after Isidore of Seville, whose *Etymologiae* (~630 AD) compiled the knowledge of the
ancient world instead of re-deriving it — the first great act of "compile, don't crawl".
"""
from __future__ import annotations

from .pipeline import CompileResult, compile_wiki
from .qa import ask

__version__ = "0.1.0"
__all__ = ["CompileResult", "__version__", "ask", "compile_wiki"]
