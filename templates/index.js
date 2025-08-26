// File input handling
        const fileInput = document.getElementById('resume');
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');
        const analyzeBtn = document.getElementById('analyze-btn');
        const btnText = document.getElementById('btn-text');
        const loadingSpinner = document.getElementById('loading-spinner');

        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                fileName.textContent = file.name;
                fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                fileInfo.classList.remove('hidden');
                
                // Add success animation
                fileInfo.classList.add('animate-pulse');
                setTimeout(() => {
                    fileInfo.classList.remove('animate-pulse');
                }, 1000);
            } else {
                fileInfo.classList.add('hidden');
            }
        });

        // Form submission handling
        document.querySelector('form').addEventListener('submit', function(e) {
            btnText.textContent = 'Analyzing...';
            loadingSpinner.classList.remove('hidden');
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('opacity-75', 'cursor-not-allowed');
        });

        // Particle animation
        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + 'vw';
            particle.style.width = Math.random() * 4 + 2 + 'px';
            particle.style.height = particle.style.width;
            particle.style.animationDuration = Math.random() * 3 + 2 + 's';
            
            document.getElementById('particles-container').appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 5000);
        }

        // Create particles periodically
        setInterval(createParticle, 300);

        // Drag and drop functionality
        const dropZone = document.querySelector('.file-input-label');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight() {
            dropZone.classList.add('bg-blue-500', 'bg-opacity-20');
        }

        function unhighlight() {
            dropZone.classList.remove('bg-blue-500', 'bg-opacity-20');
        }

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        }

        // Smooth scrolling for navigation
        document.querySelectorAll('nav button').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                // Add smooth scroll behavior if needed
            });
        });

        // Add loading animation on page load
        window.addEventListener('load', function() {
            document.body.classList.add('animate-fade-in');
        });

        // Smooth scrolling
        document.documentElement.style.scrollBehavior = 'smooth';
