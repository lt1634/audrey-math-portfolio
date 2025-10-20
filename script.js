// Language Toggle Functionality
const languageToggle = document.getElementById('language-toggle');
const body = document.body;

// Check for saved language preference or default to English
const currentLanguage = localStorage.getItem('language') || 'en';
body.setAttribute('data-lang', currentLanguage);

// Set initial toggle state
if (currentLanguage === 'zh') {
    languageToggle.checked = true;
}

// Language toggle event listener
languageToggle.addEventListener('change', function() {
    if (this.checked) {
        body.setAttribute('data-lang', 'zh');
        localStorage.setItem('language', 'zh');
        updateLanguageContent('zh');
    } else {
        body.setAttribute('data-lang', 'en');
        localStorage.setItem('language', 'en');
        updateLanguageContent('en');
    }
});

// Function to update all language content
function updateLanguageContent(lang) {
    const elements = document.querySelectorAll('[data-en][data-zh]');
    
    elements.forEach(element => {
        // Add fade out effect
        element.classList.add('language-transition', 'fade-out');
        
        setTimeout(() => {
            // Update content
            const content = element.getAttribute(`data-${lang}`);
            if (content) {
                // For all elements, use textContent to avoid HTML duplication
                element.textContent = content;
            }
            
            // Add fade in effect
            element.classList.remove('fade-out');
            element.classList.add('fade-in');
            
            // Remove transition classes after animation
            setTimeout(() => {
                element.classList.remove('language-transition', 'fade-in');
            }, 200);
        }, 100);
    });
    
    // Update form placeholders
    const placeholderElements = document.querySelectorAll('[data-en-placeholder][data-zh-placeholder]');
    placeholderElements.forEach(element => {
        const placeholder = element.getAttribute(`data-${lang}-placeholder`);
        if (placeholder) {
            element.placeholder = placeholder;
        }
    });
}

// Initialize language content
updateLanguageContent(currentLanguage);

// Dark Mode Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
body.setAttribute('data-theme', currentTheme);

// Set initial toggle state
if (currentTheme === 'dark') {
    themeToggle.checked = true;
}

// Detect system theme preference
function detectSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

// Initialize theme based on system preference if no saved preference
if (!localStorage.getItem('theme')) {
    const systemTheme = detectSystemTheme();
    body.setAttribute('data-theme', systemTheme);
    if (systemTheme === 'dark') {
        themeToggle.checked = true;
    }
}

// Listen for system theme changes
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            body.setAttribute('data-theme', newTheme);
            themeToggle.checked = e.matches;
        }
    });
}

// Theme toggle event listener
themeToggle.addEventListener('change', function() {
    if (this.checked) {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }
});

// DOM Elements
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');
const contactBtn = document.getElementById('contactBtn');
const projectsBtn = document.getElementById('projectsBtn');
const contactForm = document.getElementById('contactForm');

// Mobile Navigation Toggle
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Hero Button Interactions
contactBtn.addEventListener('click', () => {
    const contactSection = document.querySelector('#contact');
    const offsetTop = contactSection.offsetTop - 80;
    window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
    });
});

projectsBtn.addEventListener('click', () => {
    const projectsSection = document.querySelector('#projects');
    const offsetTop = projectsSection.offsetTop - 80;
    window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
    });
});

// Contact Form Handling
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(contactForm);
    const name = formData.get('name');
    const email = formData.get('email');
    const subject = formData.get('subject');
    const message = formData.get('message');
    
    // Show loading state
    const submitBtn = contactForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<span class="loading"></span> Sending...';
    submitBtn.disabled = true;
    
    // Simulate form submission (replace with actual form handling)
    setTimeout(() => {
        // Show success message
        showNotification('Message sent successfully! I\'ll get back to you soon.', 'success');
        
        // Reset form
        contactForm.reset();
        
        // Reset button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 2000);
});

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.05,
        rootMargin: '0px 0px -20px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Observe elements with fade-in class
    const animatedElements = document.querySelectorAll('.project-card, .skill-item, .about-text');
    animatedElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// Navbar scroll effect
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.background = 'var(--navbar-bg)';
            navbar.style.boxShadow = '0 2px 20px var(--shadow)';
        } else {
            navbar.style.background = 'var(--navbar-bg)';
            navbar.style.boxShadow = 'none';
        }
        
        lastScrollTop = scrollTop;
    });
}

// Typing animation for hero title
function initTypingAnimation() {
    const heroTitle = document.querySelector('.hero-title');
    const text = heroTitle.textContent;
    const highlightText = 'Tim Yuen';
    
    heroTitle.innerHTML = '';
    
    let i = 0;
    const typeWriter = () => {
        if (i < text.length) {
            if (text.substring(i, i + highlightText.length) === highlightText) {
                heroTitle.innerHTML += `<span class="highlight">${highlightText}</span>`;
                i += highlightText.length;
            } else {
                heroTitle.textContent += text.charAt(i);
                i++;
            }
            setTimeout(typeWriter, 100);
        }
    };
    
    setTimeout(typeWriter, 1000);
}

// Project card hover effects
function initProjectCardEffects() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Skill item animation on hover
function initSkillItemEffects() {
    const skillItems = document.querySelectorAll('.skill-item');
    
    skillItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'translateY(-5px) scale(1.05)';
            item.style.boxShadow = '0 8px 25px rgba(79, 70, 229, 0.15)';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateY(0) scale(1)';
            item.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Parallax effect for hero section
function initParallaxEffect() {
    const hero = document.querySelector('.hero');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxSpeed = 0.5;
        
        if (hero) {
            hero.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
        }
    });
}

// Initialize all features when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initNavbarScroll();
    initTypingAnimation();
    initProjectCardEffects();
    initSkillItemEffects();
    initParallaxEffect();
    
    // Add loading animation to page
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.3s ease';
        document.body.style.opacity = '1';
    }, 50);
});

// Handle window resize
window.addEventListener('resize', () => {
    // Close mobile menu on resize
    if (window.innerWidth > 768) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});

// Add some interactive console messages
console.log('%c👋 Hello there!', 'color: #4f46e5; font-size: 20px; font-weight: bold;');
console.log('%cThanks for checking out Tim\'s portfolio!', 'color: #6b7280; font-size: 14px;');
console.log('%cFeel free to explore the code and reach out if you have any questions.', 'color: #6b7280; font-size: 12px;');
