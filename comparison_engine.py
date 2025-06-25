from __future__ import annotations

from diff_match_patch import diff_match_patch


def compare_responses(commercial: str, local: str) -> str:
    dmp = diff_match_patch()
    diffs = dmp.diff_main(commercial, local)
    dmp.diff_cleanupSemantic(diffs)
    return dmp.diff_prettyHtml(diffs)
