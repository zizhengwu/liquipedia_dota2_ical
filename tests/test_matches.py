from datetime import UTC, datetime, timedelta
import unittest

from liquipedia_ical.matches import LiquipediaError, parse_upcoming_matches


HTML = """
<div data-toggle-area-content="1">
  <div class="match-info">
    <span class="timer-object" data-timestamp="1784286000">date</span>
    <div class="match-info-header">
      <div class="match-info-header-opponent"><span class="name">Team &amp; One</span></div>
      <div class="match-info-header-scoreholder">
        <span class="match-info-header-scoreholder-lower">(Bo3)</span>
      </div>
      <div class="match-info-header-opponent"><span class="name">Team Two</span></div>
    </div>
    <div class="match-info-tournament-name">
      <a href="/dota2/Test_League">Test League - Playoffs</a>
    </div>
    <div class="match-info-links">
      <a href="/dota2/index.php?title=Match:ID_abc_R01-M001&amp;action=edit&amp;redlink=1">details</a>
    </div>
  </div>
</div>
<div data-toggle-area-content="2">
  <div class="match-info">
    <span class="timer-object" data-timestamp="1">completed</span>
    <div class="match-info-header-opponent"><span class="name">Old One</span></div>
    <div class="match-info-header-opponent"><span class="name">Old Two</span></div>
  </div>
</div>
"""


class ParseUpcomingMatchesTest(unittest.TestCase):
    def test_parses_only_upcoming_match_cards(self) -> None:
        matches = parse_upcoming_matches(HTML)

        self.assertEqual(len(matches), 1)
        match = matches[0]
        self.assertEqual(match.start, datetime(2026, 7, 17, 11, 0, tzinfo=UTC))
        self.assertEqual(match.team1, "Team & One")
        self.assertEqual(match.team2, "Team Two")
        self.assertEqual(match.tournament, "Test League - Playoffs")
        self.assertEqual(match.series_format, "Bo3")
        self.assertEqual(match.duration, timedelta(hours=3))
        self.assertEqual(match.source_id, "Match:ID_abc_R01-M001")
        self.assertEqual(
            match.source_url,
            "https://liquipedia.net/dota2/Match:ID_abc_R01-M001",
        )

    def test_refuses_to_return_an_empty_calendar(self) -> None:
        with self.assertRaises(LiquipediaError):
            parse_upcoming_matches('<div data-toggle-area-content="1"></div>')

    def test_refuses_to_return_partial_data(self) -> None:
        malformed = HTML.replace(
            '</div>\n</div>\n<div data-toggle-area-content="2">',
            '<div class="match-info">missing required fields</div></div>\n'
            '<div data-toggle-area-content="2">',
            1,
        )

        with self.assertRaises(LiquipediaError):
            parse_upcoming_matches(malformed)


if __name__ == "__main__":
    unittest.main()
