# 🎨 HireSkill Design System

## Color Palette

### Light Theme
```css
Primary Color:      #0066cc (Blue)
Primary Hover:      #0052a3 (Dark Blue)
Primary Light:      #e6f2ff (Light Blue)

Background Primary:   #ffffff (White)
Background Secondary: #f8f9fa (Light Gray)
Background Tertiary:  #e9ecef (Gray)

Text Primary:    #212529 (Dark Gray)
Text Secondary:  #6c757d (Medium Gray)
Text Tertiary:   #adb5bd (Light Gray)

Border Color:    #dee2e6 (Light Gray)
Shadow:          rgba(0, 0, 0, 0.1)
```

### Dark Theme
```css
Primary Color:      #0066cc (Blue)
Primary Hover:      #0052a3 (Dark Blue)
Primary Light:      #001a33 (Dark Blue)

Background Primary:   #1a1a1a (Dark)
Background Secondary: #2d2d2d (Darker Gray)
Background Tertiary:  #404040 (Gray)

Text Primary:    #ffffff (White)
Text Secondary:  #b0b0b0 (Light Gray)
Text Tertiary:   #808080 (Gray)

Border Color:    #404040 (Dark Gray)
Shadow:          rgba(0, 0, 0, 0.3)
```

### Status Colors (Both Themes)
```css
Success: #28a745 (Green)
Danger:  #dc3545 (Red)
Warning: #ffc107 (Yellow)
Info:    #17a2b8 (Cyan)
```

## Typography

### Font Family
```css
Primary Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
              'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 
              'Droid Sans', 'Helvetica Neue', sans-serif

Code Font: source-code-pro, Menlo, Monaco, Consolas, 
           'Courier New', monospace
```

### Font Sizes
```css
Large Heading:   2rem (32px)
Medium Heading:  1.5rem (24px)
Small Heading:   1.3rem (20.8px)
Body Text:       1rem (16px)
Small Text:      0.9rem (14.4px)
Tiny Text:       0.85rem (13.6px)
```

### Font Weights
```css
Normal:  400
Medium:  500
Bold:    600
Extra Bold: 700
```

## Spacing System

```css
Extra Small: 0.25rem (4px)
Small:       0.5rem (8px)
Medium:      1rem (16px)
Large:       1.5rem (24px)
Extra Large: 2rem (32px)
2X Large:    3rem (48px)
```

## Border Radius

```css
Small:  0.25rem (4px)
Medium: 0.5rem (8px)
Large:  1rem (16px)
Full:   9999px (Circle)
```

## Shadows

### Light Theme
```css
Default:      0 2px 8px rgba(0, 0, 0, 0.1)
Hover:        0 4px 16px rgba(0, 0, 0, 0.15)
Large:        0 20px 60px rgba(0, 0, 0, 0.1)
```

### Dark Theme
```css
Default:      0 2px 8px rgba(0, 0, 0, 0.3)
Hover:        0 4px 16px rgba(0, 0, 0, 0.4)
Large:        0 20px 60px rgba(0, 0, 0, 0.3)
```

## Components

### Buttons

#### Primary Button
```css
Background: var(--primary-color)
Color: white
Padding: 0.85rem 1.5rem
Border Radius: 0.5rem
Font Weight: 600
Transition: all 0.3s ease

Hover:
  Background: var(--primary-hover)
  Transform: translateY(-2px)
  Box Shadow: 0 4px 12px var(--shadow-hover)
```

#### Secondary Button
```css
Background: var(--bg-secondary)
Color: var(--text-primary)
Border: 2px solid var(--border-color)
Padding: 0.85rem 1.5rem
Border Radius: 0.5rem
Font Weight: 600

Hover:
  Background: var(--bg-tertiary)
```

### Input Fields

```css
Padding: 0.75rem 1rem
Border: 2px solid var(--border-color)
Border Radius: 0.5rem
Background: var(--bg-secondary)
Color: var(--text-primary)
Font Size: 1rem
Transition: all 0.3s ease

Focus:
  Border Color: var(--primary-color)
  Background: var(--bg-primary)
  Outline: none
```

### Cards

```css
Background: var(--bg-primary)
Border Radius: 1rem
Padding: 2rem
Box Shadow: 0 2px 8px var(--shadow)
Transition: all 0.3s ease

Hover:
  Box Shadow: 0 4px 16px var(--shadow-hover)
```

### Navbar

```css
Background: var(--bg-primary)
Border Bottom: 1px solid var(--border-color)
Padding: 1rem 2rem
Box Shadow: 0 2px 8px var(--shadow)
Position: sticky
Top: 0
Z-Index: 100
```

### Badges

```css
Primary Badge:
  Background: var(--primary-light)
  Color: var(--primary-color)
  Padding: 0.25rem 1rem
  Border Radius: 9999px
  Font Size: 0.85rem
  Font Weight: 600

Success Badge:
  Background: #d4edda
  Color: #155724

Info Badge:
  Background: #d1ecf1
  Color: #0c5460
```

### Skill Tags

```css
Background: var(--bg-secondary)
Border: 1px solid var(--border-color)
Padding: 0.5rem 1rem
Border Radius: 9999px
Font Size: 0.9rem
Color: var(--text-primary)
Display: inline-flex
Align Items: center
Gap: 0.5rem
```

## Animations

### Slide Up
```css
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

Duration: 0.5s
Timing: ease
```

### Fade In
```css
Transition: opacity 0.3s ease
```

### Scale Up (Hover)
```css
Transform: scale(1.05)
Transition: transform 0.3s ease
```

### Slide Down (Hover)
```css
Transform: translateY(-2px)
Transition: transform 0.3s ease
```

## Responsive Breakpoints

```css
Mobile:      max-width: 768px
Tablet:      769px - 1024px
Desktop:     1025px+
```

### Mobile Adjustments (max-width: 768px)

```css
/* Navbar */
Padding: 1rem

/* Cards */
Padding: 1.5rem

/* Grid Layouts */
Grid Template Columns: 1fr (single column)

/* Font Sizes */
Large Heading: 1.75rem (28px)
Medium Heading: 1.25rem (20px)
```

## Layout Patterns

### Container
```css
Max Width: 1200px
Margin: 0 auto
Padding: 2rem
```

### Two Column Grid
```css
Display: grid
Grid Template Columns: 1fr 1fr
Gap: 1rem

@media (max-width: 768px) {
  Grid Template Columns: 1fr
}
```

### Flex Center
```css
Display: flex
Justify Content: center
Align Items: center
```

### Flex Between
```css
Display: flex
Justify Content: space-between
Align Items: center
```

## Accessibility

### Focus States
```css
All interactive elements have visible focus states
Focus Ring: 2px solid var(--primary-color)
Outline Offset: 2px
```

### Color Contrast
```css
Text on Light Background: Contrast Ratio > 7:1
Text on Dark Background: Contrast Ratio > 7:1
Primary Button: WCAG AAA compliant
```

### ARIA Labels
- All buttons have descriptive labels
- Form inputs have associated labels
- Navigation has proper ARIA roles
- Loading states announced to screen readers

## Icon System

### Emojis Used
```
🌙 Dark Mode
☀️ Light Mode
🔐 Security
👤 User Profile
🎨 Theme
✓ Success
✗ Error
⚠️ Warning
📧 Email
🔒 Password
```

## Form States

### Default State
```css
Border: 2px solid var(--border-color)
Background: var(--bg-secondary)
```

### Focus State
```css
Border: 2px solid var(--primary-color)
Background: var(--bg-primary)
```

### Error State
```css
Border: 2px solid var(--danger-color)
```

### Success State
```css
Border: 2px solid var(--success-color)
```

### Disabled State
```css
Opacity: 0.6
Cursor: not-allowed
```

## Loading States

### Button Loading
```css
Content: "Loading..."
Opacity: 0.7
Cursor: wait
```

### Page Loading
```css
Display: flex
Justify Content: center
Align Items: center
Height: 100vh
Font Size: 1.5rem
Color: var(--text-secondary)
```

## Error Display

### Error Message
```css
Color: var(--danger-color)
Font Size: 0.85rem
Margin Top: 0.25rem
Background: rgba(220, 53, 69, 0.1)
Padding: 0.5rem
Border Radius: 0.25rem
```

### Success Message
```css
Color: var(--success-color)
Font Size: 0.85rem
Margin Top: 0.25rem
Background: rgba(40, 167, 69, 0.1)
Padding: 0.5rem
Border Radius: 0.25rem
```

## Transitions

### Default Transition
```css
Transition: all 0.3s ease
```

### Theme Transition
```css
Transition: background-color 0.3s ease,
            color 0.3s ease,
            border-color 0.3s ease
```

### Transform Transition
```css
Transition: transform 0.3s ease
```

## Z-Index Scale

```css
Navbar:      100
Modal:       1000
Tooltip:     1100
Dropdown:    900
Overlay:     999
```

## Usage Examples

### Creating a Primary Button
```jsx
<button className="btn btn-primary btn-full">
  Sign In
</button>
```

### Creating a Card
```jsx
<div className="card">
  <div className="card-header">
    <h2>Title</h2>
  </div>
  <div className="card-body">
    Content
  </div>
</div>
```

### Creating a Form Group
```jsx
<div className="form-group">
  <label htmlFor="email">Email</label>
  <input
    type="email"
    id="email"
    name="email"
    placeholder="Enter your email"
  />
</div>
```

### Creating a Badge
```jsx
<span className="badge badge-primary">
  Active
</span>
```

### Creating Skill Tags
```jsx
<div className="skills-list">
  <span className="skill-tag">Python</span>
  <span className="skill-tag">React</span>
  <span className="skill-tag">PostgreSQL</span>
</div>
```

---

**This design system ensures consistency across the entire application and provides a foundation for future development.**
