// Main JavaScript file for Bluehawks Security Services

// WhatsApp Float Button Animation
document.addEventListener('DOMContentLoaded', function() {
    // WhatsApp float button functionality
    const whatsappFloat = document.querySelector('.whatsapp-float');
    if (whatsappFloat) {
        whatsappFloat.addEventListener('click', function(e) {
            // Add click tracking if needed
            console.log('WhatsApp button clicked');
        });
    }
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Form validation helper functions
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

function validatePhone(phone) {
    const cleanPhone = phone.replace(/[\s\-\(\)]/g, '');
    return /^(\+92|92|0)?[0-9]{10,11}$/.test(cleanPhone);
}

// Add error class to form fields
function addErrorClass(fieldName) {
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (field) {
        field.classList.add('error');
    }
}

// Remove error class from form fields
function removeErrorClass(fieldName) {
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (field) {
        field.classList.remove('error');
    }
}

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
});

// Performance optimization: Preload critical resources
function preloadCriticalResources() {
    const criticalImages = [
        '/static/images/homepage-banner.jpg',
        '/static/images/bluehawks-logo.png'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    preloadCriticalResources();
}); 