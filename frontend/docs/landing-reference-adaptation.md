# Landing reference adaptation

Approved scope: Landing Page only. The authenticated shell, learning pages and backend are not edited by this batch.

The redesigned page uses a white/green/amber palette drawn from the user's dashboard/chat references. Busuu influences the generous type hierarchy, language strip, alternating visual/copy sections, real reviews and final conversion band. Header structure is an inDrive-inspired implementation choice, explicitly not a verified pixel replica: public text retrieval and research did not reveal the current inDrive header geometry or responsive DOM.

Sources inspected: https://indrive.com/ and https://www.busuu.com/en-US ; repository reference archive under `theme/busuu/`. The inspected `50a46609ddcddf5d.css` archive file turned out to be Plyr media-player styles, not the landing layout. Its rules were not copied or falsely treated as page measurements. The Busuu layout adaptation is therefore not a pixel-exact reproduction.

## Preserved project data and functions

- Existing translated landing/common/billing strings.
- Existing session-cookie CTA routing and server-controlled registration permission.
- Existing config-backed billing, prices, trial days and PricingSection.
- Real public reviews only; no section/navigation for empty testimonials.
- Existing language listing, FAQ, contact, legal routes, metadata and repository link.
- Existing LandingNav locale links, mobile menu focus/Escape handling and scroll lock.

Config and reviews now fail independently through Promise.allSettled. Invalid review responses do not become fabricated testimonials. Structured-data metadata no longer hardcodes a zero-price offer when billing config might differ.

The new artwork is original decorative SVG with no learner identity, false scores or claimed product screenshot. No Busuu/inDrive logo, testimonial or usage metric is presented as JUBA LISAN data. The public language strip uses the existing project's featured-language component without claiming independently verified content availability for every catalog language.

## CSS isolation

All new CSS rules are rooted in `.juba-landing-refresh`. No global body/root or authenticated-shell selector is changed. New styles target the existing navigation classes only beneath that landing wrapper. Existing shared component behavior is retained; other consumers of LandingNav keep their existing presentation.

Responsive layouts include a two-column desktop hero, stacked mobile content, alternating feature blocks, RTL logical spacing, accessible navigation/CTA focus states and reduced-motion handling. The existing nav's 1001px desktop/mobile behavior is matched by the new CSS.

## Verification status

Source implementation committed directly to main under explicit user approval. Build, TypeScript, browser, screenshots, asset rendering and mobile/RTL visual checks were not run because the working environment lacks project checkout/dependencies and its sandbox has no internet access. The final design must not be called pixel-identical or visually verified. Shared FAQ/reviews/pricing inheritance and real locale text wrapping need runtime review before release.
