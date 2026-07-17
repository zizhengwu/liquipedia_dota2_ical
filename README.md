# Liquipedia Dota 2 iCalendar

This repository turns the upcoming matches shown on [Liquipedia:Matches](https://liquipedia.net/dota2/Liquipedia:Matches) into `dota2-matches.ics`. A scheduled GitHub Actions workflow refreshes it every hour and commits only when the calendar actually changes.

## Publish and subscribe

1. Push this repository to a **public** GitHub repository.
2. Open the repository's **Actions** tab, select **Update Dota 2 calendar**, and run it once with **Run workflow**. Scheduled runs then happen hourly.
3. Build the public calendar URL by replacing the placeholders:

   ```text
   https://raw.githubusercontent.com/<OWNER>/<REPOSITORY>/<DEFAULT_BRANCH>/dota2-matches.ics
   ```

4. In Google Calendar on the web, open **Other calendars → + → From URL**, paste that URL, and select **Add calendar**.

Google controls how often subscribed calendars are refreshed, so changes are not immediate. The raw URL must be publicly accessible; Google cannot subscribe to a private GitHub repository.

## Run locally

Create the project-local environment and install from the lockfile:

```powershell
uv sync --locked
$env:LIQUIPEDIA_USER_AGENT = "LiquipediaIcal/1.0 (https://github.com/YOU/REPOSITORY; mailto:you@example.com)"
uv run liquipedia-ical
```

Liquipedia requires a custom User-Agent that identifies the project and includes contact information. The GitHub workflow derives one from the repository URL automatically.

To write somewhere else:

```powershell
uv run liquipedia-ical --output public/dota2-matches.ics
```

Run the tests with:

```powershell
uv run python -m unittest discover -s tests -v
```

## Calendar behavior

- The feed contains the 50 upcoming match cards returned by the page, including TBD participants.
- Times are emitted in UTC, so Google Calendar displays them in each subscriber's local time zone.
- Liquipedia provides start times but not end times. Event lengths are estimates based on the series format: Bo1 is one hour, Bo3 is three hours, Bo5 is five hours, and an unknown format is three hours.
- Events are transparent, so they do not mark subscribers as busy.
- Stable match IDs become stable iCalendar UIDs. If a scheduled time or participant changes, the existing event is updated instead of duplicated.
- Removed or completed matches disappear on the next generated version.

## Liquipedia usage

The generator uses one gzip-enabled MediaWiki `action=parse` API request per run; it does not scrape Liquipedia's generated HTML endpoint. The hourly workflow is comfortably within Liquipedia's API rate limits. Calendar descriptions retain a source link and attribution.

Liquipedia-derived data is available under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Liquipedia's [API Terms of Use](https://liquipedia.net/api-terms-of-use) also apply.
