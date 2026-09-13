---
name: STEALTHNET Website
description: A contemporary field guide for self-hosted VPN administration.
colors:
  ink: "#102522"
  deep: "#0b1b19"
  muted: "#b7c9c2"
  mint: "#b5edca"
  line: "#324a42"
  paper: "#fafbf9"
  text: "#20352d"
  secondary: "#52675d"
  accent: "#176645"
  rule: "#dce5df"
  on-ink: "#f2f7f3"
  action-ink: "#102b20"
  docs-action: "#1e603d"
  white: "#fff"
typography:
  display:
    fontFamily: "Onest, sans-serif"
    fontSize: "clamp(52px, 6.3vw, 92px)"
    fontWeight: 550
    lineHeight: 1.12
    letterSpacing: "-.04em"
  headline:
    fontFamily: "Onest, sans-serif"
    fontSize: "clamp(34px, 3.6vw, 54px)"
    fontWeight: 550
    lineHeight: 1.12
    letterSpacing: "-.035em"
  title:
    fontFamily: "Onest, sans-serif"
    fontSize: "25px"
    fontWeight: 550
    lineHeight: 1.12
    letterSpacing: "-.02em"
  body:
    fontFamily: "Onest, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Onest, sans-serif"
    fontSize: "14px"
    fontWeight: 550
    lineHeight: 1.4
  article-title:
    fontFamily: "Onest, sans-serif"
    fontSize: "clamp(32px, 3vw, 43px)"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-.035em"
  article-body:
    fontFamily: "Onest, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.85
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "13px"
    lineHeight: 1.75
rounded:
  compact: "6px"
  control: "8px"
  button: "9px"
  code: "10px"
  surface: "12px"
  dialog: "14px"
spacing:
  8: "8px"
  12: "12px"
  16: "16px"
  20: "20px"
  24: "24px"
  28: "28px"
  40: "40px"
components:
  button-primary:
    backgroundColor: "{colors.mint}"
    textColor: "{colors.action-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "12px 21px"
  button-primary-hover:
    backgroundColor: "#d1f6de"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.on-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "12px 21px"
  button-docs-primary:
    backgroundColor: "{colors.docs-action}"
    textColor: "{colors.white}"
    rounded: "{rounded.button}"
    padding: "12px 21px"
  button-docs-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.docs-action}"
    rounded: "{rounded.button}"
    padding: "12px 21px"
  search-field:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.button}"
    padding: "13px 16px"
  nav-article:
    textColor: "{colors.secondary}"
    rounded: "{rounded.compact}"
    padding: "7px 10px"
  nav-article-current:
    backgroundColor: "#e4f0e5"
    textColor: "{colors.accent}"
  gallery-selector:
    textColor: "{colors.muted}"
    rounded: "{rounded.control}"
    padding: "10px 19px"
  gallery-selector-selected:
    backgroundColor: "#e9f4ed"
    textColor: "{colors.ink}"
  article-link-card:
    rounded: "{rounded.button}"
    padding: "18px 20px"
  article-contents:
    backgroundColor: "#f0f5ed"
    rounded: "{rounded.control}"
    padding: "13px 16px"
---

# Design System: STEALTHNET Website

## Overview

**Creative North Star: "Contemporary Field Guide"**

STEALTHNET pairs spacious product presentation with compact, carefully indexed technical reading. Deep green ink gives real product imagery a strong setting; pale paper gives instructions room to be read. Shared typography, green accents, fine rules and gently rounded controls connect these two treatments.

The character is direct, composed and practical. Authentic application screenshots provide visual evidence, while clear labels and predictable navigation carry the interface. Expression comes from type scale, image scale and the rhythm of open space and dense information. The approved black rounded-square mark with its white S is a fixed identity asset.

**Key Characteristics:**

- One locally served variable typeface for English and Russian.
- Deep ink presentation and pale paper reading surfaces within one green palette.
- Large authentic product images and precise, compact navigation.
- Fine dividing rules, flat resting surfaces and rounded interactive controls.
- Visible focus, explicit labels and navigation that survives without JavaScript.

This record is extracted from `assets/site.css`, `assets/site.js`, `build.py`, the generated English and Russian pages, and the final captures in `.impeccable/review/`. Page-specific composition and modes remain in `.impeccable/surfaces/website.md`; this file records reusable visual decisions.

## Colors

The palette moves from green-black ink through muted sage to pale mint, with quieter green text and rules on paper. The frontmatter is the normative palette; descriptive names below explain its use.

### Primary

- **Fresh Mint** (`mint`) identifies primary actions and emphasized display text against ink.
- **Reading Green** (`accent`) identifies article links, selected navigation and on-page position against paper.
- **Solid Action Green** (`docs-action`) gives filled reading-surface actions enough contrast for white labels.

### Neutral

- **Green Ink** (`ink`) is the primary presentation background; **Deep Ink** (`deep`) separates inset command surfaces and the dark footer.
- **Pale Ink Text** (`on-ink`) and **Muted Sage** (`muted`) separate primary content from supporting copy on dark surfaces. **Action Ink** (`action-ink`) is the dark label on mint controls.
- **Cool Paper** (`paper`) is the reading background. **Reading Ink** (`text`) and **Secondary Green** (`secondary`) distinguish article text from navigation and supporting information. **White** (`white`) supports inverted labels and secondary reading controls.
- **Ink Rule** (`line`) and **Paper Rule** (`rule`) separate adjacent regions without adding raised containers. The reading surface remaps the shared line and muted roles to its paper equivalents.

**The Contextual Accent Rule.** Use mint on ink and darker green on paper; retain this contrast relationship when extending either surface.

## Typography

**Display and Body Font:** Onest, with a sans-serif fallback. The variable font is served locally from `assets/fonts/onest.ttf`, preloaded by the page template, and uses `font-display: swap`. Its license is in `assets/fonts/OFL.txt`. English and Russian share the same type system.

**Code Font:** The platform monospace stack in the frontmatter. Preserve command whitespace and distinguish code from prose with its surface treatment.

The type is open and contemporary, with moderate display weight and tight heading spacing. The scale is responsive and role-based rather than a fixed mathematical ratio. Display, headline and title roles belong to presentation; article title and body roles provide the denser reading hierarchy.

- Presentation body text has a general maximum measure of (70ch). Supporting text and labels step down for secondary information.
- Article paragraphs have a maximum measure of (72ch) inside an article column capped at (820px). Article subheadings use (25px / 600) and (19px / 600); body emphasis uses weight (650).
- Compact article navigation is (12px), breadcrumbs and on-page contents are (11px). Labels use normal sentence case; the wordmark retains its uppercase identity.
- At phone widths, the landing display uses `clamp(46px, 10vw, 66px)`. Article titles use (33px); article body uses (14px / 1.85); code blocks use (11px). The search input increases to (16px) on phones.

**The Reading Measure Rule.** Let navigation use compact type, but preserve the article's open line height and bounded measure. Long commands and tables scroll within their own regions.

## Layout

Presentation content uses a centered container capped at (1344px), with (56px) side gutters at wide desktop sizes. The gutters reduce to (36px) at widths up to (1200px) and (20px) at widths up to (700px). Broad sections can pair columns; narrower viewports stack the content in reading order. Horizontal rules organize repeated feature and category rows. Section-specific column proportions remain local to their pages.

The documentation shell is capped at (1600px), with a (266px) independently scrolling category sidebar, a flexible article column and a (214px) independently scrolling on-page contents rail. The reading header stays at the top at (76px); the navigation rails sit below it. Main article padding is (34px) above, (80px) below, with fluid horizontal space from (24px) to (65px).

- Up to (1200px), documentation uses a (242px) category sidebar and hides the right rail. An explicit **On this page** disclosure appears below the article title, keeping the heading links available.
- Up to (920px), presentation column pairs stack and the documentation directory becomes one column. Optional header content progressively contracts.
- Up to (700px), the reading header becomes (66px), the main article uses (20px) side gutters, and **Contents** exposes categorized site navigation above the breadcrumbs. The separate **On this page** disclosure remains within the article. Both use native details/summary behavior and bounded internal scrolling.
- Article pagination uses two equal columns with a (16px) gap, reducing spacing on phones. Tables and preformatted code preserve their content width inside scrolling regions.

Spacing comes from a compact control rhythm and a much more open section rhythm. Use the extracted spacing steps for recurring controls; use the existing page structure when choosing larger section gaps.

## Elevation & Depth

Resting pages are predominantly flat. Background changes, borders, image scale and generous spacing establish depth. Native modal dialogs add a broad dark shadow and a dimmed backdrop; the copy-feedback toast uses a smaller shadow. These are transient layers, not a general card style. The exact shadow and backdrop values are recorded in the sidecar.

**The Flat Resting Surface Rule.** Use rules and tonal separation for ordinary page structure. Reserve the established shadows for modal and feedback layers.

## Shapes

Controls are gently rounded rectangles. The frontmatter records the recurring compact, control, button, code, surface and dialog radii; use the role rather than a single radius everywhere. Screenshot plates clip at their boundary, while portrait images remain contained and fully visible. Category and feature lists primarily use horizontal rules instead of individually boxed cards.

Icons are inline SVG line drawings with rounded stroke ends, typically (15–20px), using the surrounding text color. The website logo and favicon are exceptions: reuse `assets/logo.svg` and `assets/favicon.svg` as supplied. Their white S path comes from the panel's `web/core.js`, on the owner-approved black rounded square; do not redraw or recolor it.

## Components

### Buttons and action links

Confident filled controls sit beside quieter outlined actions. Shared buttons align a label and small icon, with a minimum height of (50px), a (14px) gap and the frontmatter padding. Hover changes background and border over (160ms), without moving the control. The reading variants use a minimum height of (44px), smaller labels and darker green fills; phone and header variants compact their spacing in context.

Keyboard focus uses a visible warm outline (3px, offset 4px) on buttons, links, inputs and summaries. Disabled buttons show a waiting cursor and reduced opacity. Keep text labels on primary actions. Icon-only search and close controls retain explicit localized accessible names.

### Navigation and language

The shared header anchors the wordmark, project/docs destinations and a compact language control. The current primary destination gains a colored underline. English and Russian language links always retain the counterpart article or category path; each has a localized accessible name and language metadata.

Categorized documentation uses native disclosure groups. The current article is green on a pale selected surface and marked with `aria-current`; its group opens by default. Breadcrumbs retain the category context. On-page links occupy the right rail on wide screens and the **On this page** disclosure on narrower screens. The desktop rail can highlight the currently visible heading.

### Search

A localized search trigger opens a native dialog. The search field has a persistent accessible name independent of its placeholder, an inset search icon and a green focus-within outline. Results show category, title and excerpt, with matched text highlighted. Title matches rank above category and body matches; the presentation remains a ranked list with a category label on every result.

The dialog supports the keyboard shortcut (Command/Ctrl+K), arrow movement through results, Enter to follow a result, Escape and an explicitly labeled close control. Loading, no-results and load-failure messages use a status region, with category browsing still available. Search indexes are local and language-specific.

### Product gallery

The selector is a row of rounded links with a pale selected state. On phones it remains on one horizontally scrollable line. Selecting the panel, storefront, customer account or Mini App changes the image, heading and explanatory caption together. The large image links to a full-image dialog; without JavaScript, image and selector links still open their real asset URLs.

Keep the four actual product views in both languages, their demonstration-data caption, and their existing origin sidecars (`assets/media/*.png.json`). The gallery's images come from the software repository's sanitized demonstration captures; their pictured application styling is evidence, not the website's token source. Use containment for portrait images and retain meaningful image alternatives.

The gallery's brief exposure animation lasts (350ms) with the shared easing curve. It changes brightness and opacity without shifting layout. Reduced-motion preference removes animation and transitions and disables smooth scrolling. Content is visible at rest.

### Reading blocks and related links

Article content uses underlined green links, shaded inline code, dark command blocks, pale table headers and quiet bordered callouts. Copy controls sit in the command block's reserved top area. Success changes the button label and announces a toast; failure asks the reader to copy manually, leaving the original command visible. Table enhancement creates a labeled, keyboard-focusable scrolling region.

Category directories use ruled text groups; category article lists use full-width linked rows. Previous/next reading links are lightly outlined rounded cards with a small directional label, article title and arrow. Hover strengthens their border and adds a pale tint. Article metadata and source-edit links remain visually secondary.

## Do's and Don'ts

### Do:

- **Do** use the local Onest font and the same hierarchy for English and Russian.
- **Do** retain the exact approved white S on its black rounded square in the logo and favicon.
- **Do** use actual product captures with their demonstration labels and origin sidecars.
- **Do** keep language links on the equivalent page and keep both category contents and article contents available at narrow widths.
- **Do** preserve visible keyboard focus, persistent accessible control names and native link/disclosure behavior.
- **Do** keep article text readable without JavaScript and use scripts to enhance search, copying and image viewing.

### Don't:

- **Don't** replace the owner-approved logo with the angular release icon or an approximation.
- **Don't** treat screenshot UI colors or isolated page adjustments as global website tokens.
- **Don't** add invented customer figures, ratings, telemetry or testimonials as visual proof.
- **Don't** turn every content group into a shadowed card; follow the established rules and tonal divisions.
- **Don't** hide navigation meaning in an icon or placeholder, or remove article contents when the desktop rail disappears.
- **Don't** make entrance animation a prerequisite for seeing content or ignore reduced-motion preference.
