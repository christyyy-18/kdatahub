# K-DataHub JavaScript Documentation

## Overview
The JavaScript file (`main.js`) provides a complete, error-free, and fully responsive functionality layer for the K-DataHub platform. It includes mobile navigation, form validation, animations, and accessibility features.

## Features

### 1. **Mobile Menu Toggle** 
- Automatically creates a hamburger menu on mobile devices (max-width: 768px)
- Smooth hamburger animation with the menu toggle
- Auto-closes menu when a navigation link is clicked
- Touch-friendly and accessible

### 2. **Smooth Scrolling**
- Smooth navigation between page sections
- Supports internal anchor links (#section-id)
- Responsive and hardware-accelerated

### 3. **Advanced Form Validation**
- **Real-time validation** as user types
- **Blur validation** for lost focus
- **Submit validation** before form submission

**Supported Field Types:**
- Text fields (required check)
- Email fields (format validation)
- Phone numbers (format and length validation)
- Numbers (valid number check)
- Passwords (minimum 8 characters)
- Textareas (required check)
- Select dropdowns (required check)

**Validation Features:**
- Custom error messages
- Visual error indicators (red border, background)
- Error messages appear below fields
- Automatic scroll to first error on submit
- Success message on valid submission

### 4. **Scroll Animations**
- Cards fade in and slide up when they come into view
- Uses IntersectionObserver API for performance
- Fallback for older browsers
- Smooth transitions

### 5. **Navbar Scroll Effect**
- Navbar shadow increases on scroll
- Visual feedback when user scrolls down
- Helps with visual hierarchy

### 6. **Button Ripple Effect**
- Ripple animation on button clicks
- Applies to all `.btn` and `button[type="submit"]` elements
- Material Design-inspired effect
- Performance optimized

## File Structure

```
kdatahub/
├── static/
│   ├── css/
│   │   ├── styles.css          # Main styles
│   │   └── js-effects.css      # JavaScript-related styles
│   ├── js/
│   │   └── main.js             # Main JavaScript file
│   └── ...
└── templates/
    └── base.html               # Base template (updated with CSS)
```

## Setup Instructions

### 1. Include Files in Your Template

Add these files to your template (Already included in base.html):

```html
<!DOCTYPE html>
<html>
<head>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    <link rel="stylesheet" href="{% static 'css/js-effects.css' %}">
</head>
<body>
    <!-- Your content -->
    
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

### 2. Required HTML Structure

#### Navigation Structure
```html
<nav class="navbar">
    <div class="nav-container">
        <div class="logo">
            <h2>Your Logo</h2>
        </div>
        <ul class="nav-links">
            <li><a href="#section1">Link 1</a></li>
            <li><a href="#section2">Link 2</a></li>
        </ul>
    </div>
</nav>
```

#### Form Structure
```html
<form>
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
    </div>
    
    <div class="form-group">
        <label for="phone">Phone</label>
        <input type="tel" id="phone" name="phone">
    </div>
    
    <div class="form-group">
        <label for="message">Message</label>
        <textarea id="message" name="message" required></textarea>
    </div>
    
    <button type="submit">Send</button>
</form>
```

#### Cards for Scroll Animation
```html
<div class="card">
    <h2>Feature Title</h2>
    <p>Feature description</p>
</div>
```

## Validation Rules

| Field Type | Required | Rules |
|-----------|----------|-------|
| Text | Yes | Not empty |
| Email | Yes | Valid email format |
| Phone | No | Valid phone format, min 7 digits |
| Number | No | Valid number, >= 0 |
| Password | No | Min 8 characters |
| Textarea | Yes | Not empty |
| Select | Yes | Option selected |

## CSS Classes Reference

### Error Handling
- `.error` - Applied to input when invalid
- `.error-message` - Error message display
- `.success-message` - Success notification

### Animations
- `.visible` - Applied when card is in view
- `.ripple` - Ripple effect indicator
- `.active` - Active state for menu

### States
- `.scrolled` - Navbar has scroll effect
- `.menu-toggle.active` - Mobile menu is open
- `.nav-links.active` - Mobile menu visible

## Customization

### Change Validation Rules
Edit the `validateField()` function in `main.js`:

```javascript
} else if (field.name === 'password' && value.length < 8) {
    // Change "8" to your desired minimum length
    isValid = false;
    errorMessage = 'Password must be at least 8 characters';
}
```

### Change Animation Duration
Edit `js-effects.css`:

```css
.card {
    transition: all 0.6s ease; /* Change 0.6s to desired duration */
}
```

### Change Ripple Effect Color
Edit `js-effects.css`:

```css
.ripple {
    background: rgba(255, 255, 255, 0.6); /* Adjust color and opacity */
}
```

## Browser Support

- **Modern Browsers**: Full support (Chrome, Firefox, Safari, Edge)
- **Mobile**: iOS 12+, Android 5+
- **IE11**: Basic support (no IntersectionObserver animations)
- **Accessibility**: WCAG 2.1 AA compliant

## Responsive Breakpoints

- **Mobile**: Max-width 768px
  - Hamburger menu appears
  - Single column layout
  - Touch-friendly buttons
  
- **Tablet**: 768px - 1024px
  - Adaptive layout
  - Normal navigation
  
- **Desktop**: 1024px+
  - Full navigation
  - Multi-column layouts

## Performance

- **IIFE Pattern**: Avoids global scope pollution
- **Event Delegation**: Minimizes event listeners
- **IntersectionObserver**: Efficient scroll animations
- **Debounced Resize**: Prevents excessive reflow
- **CSS Transforms**: Hardware-accelerated animations

## Accessibility Features

- Keyboard navigation support
- ARIA labels on interactive elements
- Focus management
- Reduced motion preferences respected
- Screen reader friendly

## Error Handling

The code includes comprehensive error handling:
- Try-catch blocks for initialization
- Console logging for debugging
- Graceful degradation for older browsers
- Invalid form submissions prevented
- Detailed error messages

## Debug Mode

Open browser console to see debug information:
```
K-DataHub Loaded Successfully
Version: 1.0.0
```

## Common Issues & Solutions

### Mobile menu not working?
- Ensure viewport meta tag is present
- Check that nav structure matches requirements
- Verify CSS file is loaded

### Form validation not working?
- Check input names and types are correct
- Ensure form has `<button type="submit">`
- Verify js-effects.css is loaded for styling

### Animations not smooth?
- Check browser support
- Verify CSS file is loaded
- Disable browser extensions that might interfere

### Ripple effect not visible?
- Ensure button has `.btn` or `type="submit"`
- Check z-index conflicts
- Verify js-effects.css is loaded

## Testing

To test functionality:

1. **Mobile Menu**: Resize window to 768px or less
2. **Form Validation**: Try submitting invalid data
3. **Animations**: Scroll page to see cards animate in
4. **Ripple Effect**: Click any button
5. **Smooth Scroll**: Click navigation links

## Updates & Maintenance

- Keep dependencies updated
- Test on new browser versions
- Monitor performance metrics
- Review console for errors
- Update WCAG compliance regularly

## Support

For issues or questions:
1. Check browser console for errors
2. Verify HTML structure matches requirements
3. Ensure all CSS and JS files are loaded
4. Check file paths in static files configuration
5. Clear browser cache and reload

## License

This JavaScript framework is part of the K-DataHub project.

---

**Last Updated**: April 2024
**Version**: 1.0.0
