# Les Petites Mains de Lisa — Design System

**Date**: 2026-06-16  
**Project**: Website Redesign - Wellness & Beauty Services  
**Business**: At-home massage, skincare, Bach Flowers, gift packages (Réunion Island)  
**Design Direction**: Minimalisme chaleureux avec caractère naturel  
**Architecture**: Scroll Narratif Fluide

---

## Design Philosophy

Reject generic AI aesthetics. Create a **distinctive, production-grade website** that maintains the warmth and accessibility of wellness while adding memorable character through:
- **Bold aesthetic direction**: Warm minimalism with natural textures
- **Distinctive typography**: Serif elegance + clean sans-serif
- **Cohesive color palette**: Soft neutrals + rich earth tones
- **Impactful animations**: Scroll reveals, stagger effects, micro-interactions
- **Creative spatial composition**: Asymmetric layouts, intentional whitespace
- **Atmospheric details**: Textures, subtle gradients, visual hierarchy

---

## Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Off-white/Cream | #F9F7F4 | Main page background |
| Primary Accent | Warm Terracotta | #C97C5C | Buttons, accents, 5★ ratings |
| Secondary Accent | Sage Green | #8FA39A | Alt accents, service dividers |
| Tertiary Accent | Warm Ocre | #D4A574 | Highlights, graphic elements |
| Text Primary | Charcoal Gray | #2C2C2C | Headings, body text |
| Text Secondary | Medium Gray | #666666 | Secondary text, captions |
| Card Background | White | #FFFFFF | Service cards, testimonials |
| Footer Background | Dark Sage/Charcoal | #3D3D3D or #5A6F6D | Footer |

**Palette Logic**: Warm, earthy palette that evokes nature, calm, and wellness. Rejects cool corporate blues/purples. Feels personal and authentic.

---

## Typography

### Typefaces
- **Headings (H1-H3)**: Serif, elegant, distinctive
  - Recommendation: **Cormorant Garamond** (700/400 weight) or **Playfair Display** (semi-bold)
  - Usage: Hero tagline, section titles, service names, testimonial quotes
  
- **Body Text**: Clean, readable sans-serif
  - Recommendation: **Inter** (400/500) or **Poppins** (regular/medium)
  - Usage: Paragraphs, descriptions, footer content

- **Accents**: Serif italic for quotes
  - Usage: Testimonial quotes

### Scale & Hierarchy
```
H1 (Hero): 4rem / 5rem (mobile: 2.5rem)
H2 (Sections): 2.5rem (mobile: 1.75rem)
H3 (Cards): 1.5rem
Body: 1rem / 1.125rem (18-20px comfortable reading)
Small: 0.875rem (captions, labels)
```

---

## Layout Structure

### Navigation
- **Type**: Sticky navigation bar
- **Style**: Logo + menu links (Services, Qui suis-je, Avis, Réserver)
- **Background**: Transparent initially, semi-transparent white/cream on scroll
- **Animation**: Smooth fade-in background color on scroll down
- **Mobile**: Hamburger menu (minimal, no dropdown bloat)

---

### Section 1: Hero
- **Height**: Full viewport or hero-tall (80vh min)
- **Background**: Atmospheric wellness image (massage/spa ambiance)
- **Overlay**: Subtle dark overlay (30% opacity) for text readability
- **Content**: 
  - Tagline: "Détente à domicile" (serif, large, centered)
  - Subtext: "Massage • Soins • Bien-être" (sans-serif, smaller)
- **Animation**: 
  - Fade-in text on page load (staggered)
  - Subtle parallax on background image (20-30% scroll)
  - Scroll indicator at bottom (animated chevron)

---

### Section 2: Qui est Lisa?
- **Layout**: Asymmetric two-column (image left, text right)
  - Desktop: 40% image | 60% text
  - Mobile: Stacked vertically
- **Image**: Portrait photo, square format (~300px), subtle shadow/border
- **Text Content**:
  - Heading: "À propos de moi" (serif)
  - Bio: ~150 words, warm & authentic tone
  - Years of experience badge (small accent element)
- **Design Details**:
  - Background: Cream (#F9F7F4)
  - Accent element: Curved line or small dot in terracotta color
  - Padding: Generous (120px top/bottom)
- **Animation**: 
  - Photo: scale-up + fade-in on scroll (from 0.95 → 1)
  - Text: fade-in with slight delay

---

### Section 3: Nos Services
- **Layout**: **Asymmetric grid** (reject standard 3x1)
  - Desktop: 
    - Row 1: Service 1 (50%) + Service 2 (50%)
    - Row 2: Service 3 (33%) + Service 4 (67%, offset right)
  - Tablet: 2x2 grid
  - Mobile: 1 column, stacked
  
- **Service Card**:
  - Dimensions: Responsive, min 250px
  - Icon: Large, custom (not generic emoji)
  - Title: Serif, 1.5rem
  - Description: Sans-serif, 1rem, 2-3 lines
  - Border: Thin left border (terracotta or sage green, alternating)
  - Background: White
  - Hover Effect: 
    - Background tints slightly toward accent color
    - Subtle shadow deepens
    - Text color shifts slightly
  - Padding: 2rem
  
- **Spacing Between Cards**: 2rem gap
- **Background Section**: White or very light cream
- **Animation**: 
  - Stagger effect: each card fades-in + slides up with 100-150ms delay
  - On scroll, each card triggers slightly different animation timing

---

### Section 4: Testimonials
- **Layout**: **Masonry/Alternating** (NOT carousel)
  - Desktop: 3-col layout, staggered heights
    - Row 1: Testimonial 1 (left) + Testimonial 2 (right) + space
    - Row 2: space + Testimonial 3 (center) + space
  - Mobile: 1 column, stacked
  
- **Testimonial Card**:
  - Star Rating: 5★ in terracotta color
  - Quote: Serif italic, 1.125rem, max 150 characters
  - Author: Sans-serif, bold, "Vérifié" badge in smaller text
  - Background: Very light (rose poudré #FFF0F3 or light cream)
  - Border Left: Thin (2px) terracotta or sage green
  - Padding: 1.5rem
  - Card shadow: Subtle (0 4px 12px rgba(0,0,0,0.08))
  
- **Animation**: 
  - Fade-in on scroll (0.6s ease-out)
  - Subtle parallax shift on scroll (y-offset ±10px)

---

### Section 5: Booking CTA
- **Layout**: Centered, with breathing room
- **Content**:
  - Heading: "Prêt à vous détendre?" (serif, 2rem)
  - Subtext optional: "Réservez votre soin en quelques clics" (sans-serif)
  - Primary Button: "Réserver maintenant" 
    - Background: Terracotta (#C97C5C)
    - Text: White, sans-serif bold
    - Padding: 1rem 2.5rem
    - Border radius: 4px (minimal, not rounded)
    - Hover: Darker terracotta + slight shadow lift
    - Animation: Smooth background color transition (0.3s)
  - Secondary Link: "Ou contactez-moi directement" (text link in gray)
  
- **Background**: Subtle gradient (cream → very light sage green) OR solid very light sage
- **Padding**: 4rem top/bottom, 2rem sides
- **Animation**: Button entrance (scale-up + fade on load)

---

### Section 6: Footer
- **Layout**: 3-column grid (desktop), single column (mobile)
- **Columns**:
  1. **Brand**: Logo + tagline (one line max)
  2. **Contact**: 
     - Icon + Phone number (clickable tel: link)
     - Icon + Email (mailto: link)
     - Horaires d'ouverture
  3. **Links**: Quick nav (Services, Bio, Avis, Réserver)
  
- **Design**:
  - Background: Dark (charcoal #3D3D3D or dark sage #5A6F6D)
  - Text: Off-white/cream
  - Icons: Terracotta color
  - Dividers: Subtle lines between columns (desktop only)
  - Padding: 2.5rem
  
- **Animation**: Fade-in on scroll

---

## Responsive Design

### Breakpoints
- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px+

### Key Changes
- **Hero**: Text size reduces, tagline 2.5rem on mobile
- **Services Grid**: 1 column on mobile, 2 on tablet
- **Testimonials**: Single column on mobile
- **Spacing**: Reduces (120px → 60px padding)
- **Navigation**: Hamburger menu on mobile

---

## Animations & Interactions

### Scroll Animations
- **Fade-in**: Elements fade from opacity 0 → 1 (0.6s ease-out)
- **Slide-up**: Y-position translate from 30px → 0 (0.6s ease-out)
- **Stagger**: Sequential animations with 100-150ms delay per item
- **Parallax**: Background images move at different speed than foreground (20-30% of scroll speed)
- **Scale**: Subtle scale-up on entrance (0.95 → 1)

### Hover Effects
- **Buttons**: Background color shift + shadow lift (0.3s)
- **Service Cards**: Background tint + shadow deepen
- **Links**: Color shift (gray → terracotta) + underline appear

### Micro-interactions
- **Scroll Indicator**: Animated chevron in hero (pulse or bounce)
- **Form Focus**: Input border color changes to accent on focus
- **CTA Button**: Slight lift effect on hover (transform: translateY(-2px))

---

## Typography Scale & Spacing

### Spacing System (8px base)
- xs: 0.5rem (8px)
- sm: 1rem (16px)
- md: 1.5rem (24px)
- lg: 2rem (32px)
- xl: 3rem (48px)
- xxl: 4rem+ (64px+)

### Line Height
- Headings: 1.2
- Body: 1.6
- Small text: 1.5

---

## Accessibility & Performance

### Accessibility
- **Color contrast**: All text meets WCAG AA standards (4.5:1 for body, 3:1 for large text)
- **Alt text**: All images have descriptive alt text
- **Focus states**: Visible focus rings on interactive elements
- **Semantic HTML**: Proper heading hierarchy (h1 → h2 → h3)

### Performance
- **Image optimization**: Responsive images with srcset, WebP format
- **CSS animations**: Use GPU-accelerated properties (transform, opacity)
- **Lazy loading**: Below-the-fold images lazy-load
- **Font loading**: System fonts or optimized Google Fonts (max 2 typefaces)

---

## Technical Stack (Implementation)

- **HTML5**: Semantic markup
- **CSS3**: Custom properties (CSS variables), Grid, Flexbox
- **JavaScript**: Vanilla JS or lightweight library (Intersection Observer for scroll animations)
- **Animation Library**: Optional GSAP or AOS.js for scroll effects (if not CSS-only)
- **Responsive**: Mobile-first approach
- **SEO**: Structured data (schema.org for Local Business)

---

## Success Criteria

✅ Site is distinctive and memorable (rejects generic AI aesthetics)  
✅ Typography is bold and intentional (serif + sans-serif pairing)  
✅ Color palette is cohesive and warm (no corporate blues)  
✅ Animations are smooth and purposeful (not gratuitous)  
✅ Spatial composition is creative and asymmetric  
✅ Booking CTA is clear and accessible  
✅ Mobile-first responsive design  
✅ Fast load time (<3s on 3G)  
✅ All accessibility standards met  

---

## Project Structure

```
lespetitesmainsdelisa-optimized/
├── index.html
├── css/
│   ├── variables.css
│   ├── reset.css
│   ├── typography.css
│   ├── layout.css
│   ├── components.css
│   └── animations.css
├── js/
│   ├── main.js
│   └── scroll-animations.js
├── assets/
│   ├── images/
│   ├── icons/
│   └── fonts/
├── Dockerfile
├── nginx.conf
└── README.md
```

---

## Next Steps

1. ✅ Design approved
2. → Create implementation plan with writing-plans skill
3. → Build HTML structure
4. → Style with CSS (variables, responsive)
5. → Add scroll animations
6. → Optimize images
7. → Deploy to Coolify
8. → Test on real devices

---

**Design authored with Frontend Design skill principles.**  
**Status**: Ready for implementation
