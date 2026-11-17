# Keeping the guide current

All content lives in `build/build.py`, between the line `CS = "https://careersourcetampabay.com"` and the
`page furniture` comment. `build/html_build.py` turns the same content into `index.html`. Never edit `index.html` by hand.

To rebuild: `sh build/rebuild.sh` from the repo root, then commit `index.html`, the PDF and `build/`.

## Weekly refresh checklist
1. Meetups, "Coming up": remove events whose date has passed. Add new ones from tampa.dev, the latest Global Nerdy
   weekly list, Tech Success Network, GDG Tampa Bay and SCORE Pinellas County. Keep events that help a junior web
   developer, job seeker or freelancer. Only list a date that appears on an organizer's or calendar's own page.
2. Freelancing, "SCORE workshops coming up": same treatment.
3. Check every link in the guide. Fix or remove any that fail. If a page cannot be checked automatically, leave it
   and list it in the commit message.
4. Employers: confirm each job page still loads. Update the "good to know" text only when the page itself shows a change.
5. Update `CHECKED` in `build/build.py` to the date of the refresh, and the "Confirm before you go" note.
6. Rebuild, look at the PDF page breaks (no heading or single line stranded on a page), commit and push to `main`.

## House rules
- No student names anywhere. Contact is Marianne Shaffer, SHAFFERMA@pcsb.org.
- Plain, direct wording. No em dashes.
- Do not list events held at bars or breweries.
- No Career Rocket and no placement coordinator references.
- Use official PTC program names.
- Keep the PTC colors, fonts and logo exactly as they are.
