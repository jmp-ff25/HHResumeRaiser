from __future__ import annotations

import unittest

from hh_raiser.activities.resume_index_refresher import (
    ResumeMarkerState,
    build_marked_description,
    restore_marked_description,
)


class ResumeIndexRefresherTests(unittest.TestCase):
    def test_marker_adds_exactly_one_period(self) -> None:
        marked, state = build_marked_description("Описание.", target_index=2)

        self.assertEqual(marked, "Описание..")
        self.assertEqual(state.target_index, 2)

    def test_restores_only_matching_marked_description(self) -> None:
        marked, state = build_marked_description("Описание.", target_index=0)

        self.assertEqual(restore_marked_description(marked, state), "Описание.")
        self.assertIsNone(restore_marked_description("Изменено вручную.", state))

    def test_rejects_inconsistent_marker_hashes(self) -> None:
        state = ResumeMarkerState(target_index=0, base_hash="bad", marked_hash="bad")

        self.assertIsNone(restore_marked_description("Описание..", state))
