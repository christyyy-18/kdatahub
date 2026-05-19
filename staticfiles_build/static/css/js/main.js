/**
 * K-DataHub Main JavaScript
 * Handles responsive navigation, form validation, animations, and interactions
 */

(function () {
    'use strict';

    // =====================
    // DOM Elements
    // =====================
    const navbar = document.querySelector('.navbar');
    const navContainer = document.querySelector('.nav-container');
    const navLinks = document.querySelectorAll('.nav-links a');
    const form = document.querySelector('form');
    const submitBtn = document.querySelector('button[type="submit"]');

    // =====================
    // Mobile Menu Toggle
    // =====================
    function initMobileMenu() {
        const menuToggle = document.createElement('button');
        menuToggle.className = 'menu-toggle';
        menuToggle.setAttribute('aria-label', 'Toggle menu');
        menuToggle.innerHTML = '<span></span><span></span><span></span>';

        // Only add menu toggle on mobile
        if (window.innerWidth <= 768) {
            const logo = document.querySelector('.logo');
            if (logo && !document.querySelector('.menu-toggle')) {
                navContainer.insertBefore(menuToggle, navContainer.querySelector('.nav-links'));
            }
        }

        menuToggle.addEventListener('click', function () {
            const navList = document.querySelector('.nav-links');
            navList.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });

        // Close menu when clicking on a link
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                document.querySelector('.nav-links').classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });
    }

    // =====================
    // Smooth Scrolling
    // =====================
    function initSmoothScroll() {
        navLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href && href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    // =====================
    // Form Validation
    // =====================
    function initFormValidation() {
        if (!form) return;

        const inputs = form.querySelectorAll('input, select, textarea');

        // Validate individual field
        function validateField(field) {
            const value = field.value.trim();
            const type = field.type;
            let isValid = true;
            let errorMessage = '';

            if (value === '') {
                isValid = false;
                errorMessage = 'This field is required';
            } else if (type === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    isValid = false;
                    errorMessage = 'Please enter a valid email address';
                }
            } else if (type === 'tel') {
                const phoneRegex = /^[\d\s\-\+\(\)]+$/;
                if (!phoneRegex.test(value) || value.length < 7) {
                    isValid = false;
                    errorMessage = 'Please enter a valid phone number';
                }
            } else if (type === 'number') {
                if (isNaN(value) || value < 0) {
                    isValid = false;
                    errorMessage = 'Please enter a valid number';
                }
            } else if (field.name === 'password' && value.length < 8) {
                isValid = false;
                errorMessage = 'Password must be at least 8 characters';
            }

            // Update field styling
            if (isValid) {
                field.classList.remove('error');
                removeErrorMessage(field);
            } else {
                field.classList.add('error');
                showErrorMessage(field, errorMessage);
            }

            return isValid;
        }

        // Show error message
        function showErrorMessage(field, message) {
            removeErrorMessage(field);
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
        }

        // Remove error message
        function removeErrorMessage(field) {
            const existingError = field.parentNode.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
        }

        // Real-time validation on input
        inputs.forEach(input => {
            input.addEventListener('blur', function () {
                validateField(this);
            });

            input.addEventListener('input', function () {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });

        // Form submission
        form.addEventListener('submit', function (e) {
            // Validate all fields
            let isFormValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isFormValid = false;
                }
            });

            if (!isFormValid) {
                e.preventDefault(); // Stop submission only if invalid
                scrollToFirstError();
            }
            // If valid, we let the event continue so Django can process the data
        });
    }

    // Show form success message
    function showFormSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        form.insertBefore(successDiv, form.firstChild);

        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }

    // Scroll to first error field
    function scrollToFirstError() {
        const firstError = form.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstError.focus();
        }
    }

    // =====================
    // Scroll Animations
    // =====================
    function initScrollAnimations() {
        const cards = document.querySelectorAll('.card');

        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, {
                threshold: 0.1
            });

            cards.forEach(card => {
                observer.observe(card);
            });
        } else {
            // Fallback for older browsers
            cards.forEach(card => {
                card.classList.add('visible');
            });
        }
    }

    // =====================
    // Navbar Scroll Effect
    // =====================
    function initNavbarScroll() {
        let lastScrollTop = 0;

        window.addEventListener('scroll', function () {
            const scrollTop = window.scrollY || document.documentElement.scrollTop;

            if (navbar) {
                if (scrollTop > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }

            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        });
    }

    // =====================
    // Button Ripple Effect
    // =====================
    function initRippleEffect() {
        const buttons = document.querySelectorAll('.btn, button[type="submit"]');

        buttons.forEach(button => {
            button.addEventListener('click', function (e) {
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');

                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';

                this.appendChild(ripple);

                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // =====================
    // Responsive Initialization
    // =====================
    function handleResize() {
        const width = window.innerWidth;

        if (width <= 768) {
            if (!document.querySelector('.menu-toggle')) {
                const menuToggle = document.createElement('button');
                menuToggle.className = 'menu-toggle';
                menuToggle.setAttribute('aria-label', 'Toggle menu');
                menuToggle.innerHTML = '<span></span><span></span><span></span>';

                const logo = document.querySelector('.logo');
                if (logo) {
                    navContainer.insertBefore(menuToggle, navContainer.querySelector('.nav-links'));
                }
            }
        } else {
            const menuToggle = document.querySelector('.menu-toggle');
            if (menuToggle) {
                menuToggle.remove();
            }
            const navList = document.querySelector('.nav-links');
            if (navList) {
                navList.classList.remove('active');
            }
        }
    }

    // =====================
    // Error Handling
    // =====================
    window.addEventListener('error', function (e) {
        console.error('Error:', e.message);
    });

    // =====================
    // Print function for console
    // =====================
    function initDebugInfo() {
        console.log('%c K-DataHub Loaded Successfully', 'color: #667eea; font-size: 16px; font-weight: bold;');
        console.log('%c Version: 1.0.0', 'color: #764ba2; font-size: 12px;');
    }

    // =====================
    // Initialize All
    // =====================
    function init() {
        try {
            initMobileMenu();
            initSmoothScroll();
            // initFormValidation(); // Disabled for Django submission
            initScrollAnimations();
            initNavbarScroll();
            initRippleEffect();
            initDebugInfo();

            window.addEventListener('resize', handleResize);
        } catch (error) {
            console.error('Initialization error:', error);
        }
    }

    // =====================
    // DOM Ready
    // =====================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
