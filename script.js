document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const iconGrid = document.getElementById('iconGrid');
    const downloadBtn = document.getElementById('downloadBtn');
    const sourceCheckboxes = document.querySelectorAll('input[name="source"]');
    const dropdownBtn = document.querySelector('.source-dropdown-btn');
    const dropdownContent = document.querySelector('.source-dropdown-content');
    let icons = [];
    let selectedIcons = new Set();
    let currentDisplayCount = 500; // Track how many icons are currently displayed

    // Optimized search with result limiting and caching
    function performOptimizedSearch(term) {
        const lowerTerm = term.toLowerCase().trim();
        if (lowerTerm.length === 0) return icons;
        
        const results = [];
        
        // Use a more efficient search approach
        for (let i = 0; i < icons.length; i++) {
            const icon = icons[i];
            
            // Quick checks first
            if (icon.name.toLowerCase().includes(lowerTerm) || 
                icon.key.toLowerCase().includes(lowerTerm)) {
                results.push(icon);
                continue;
            }
            
            // Check tags
            if (icon.tags) {
                for (let j = 0; j < icon.tags.length; j++) {
                    if (icon.tags[j].toLowerCase().includes(lowerTerm)) {
                        results.push(icon);
                        break;
                    }
                }
            }
        }
        
        return results;
    }

    // Toggle dropdown on button click
    dropdownBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isVisible = dropdownContent.style.display === 'block';
        dropdownContent.style.display = isVisible ? 'none' : 'block';
    });

    // Prevent dropdown from closing when clicking inside
    dropdownContent.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        dropdownContent.style.display = 'none';
    });

    // Load icons from JSON file
    fetch('icons.json')
        .then(response => response.json())
        .then(data => {
            console.log('Icons loaded:', data);
            // Handle both array format and object with icons property
            const iconsData = Array.isArray(data) ? data : data.icons;
            icons = iconsData.map(icon => ({
                ...icon,
                path: `icons/${icon.filename}`
            }));
            console.log('Processed icons:', icons);
            
            displayIcons();
        })
        .catch(error => {
            console.error('Error loading icons:', error);
        });

    // Display icons in the grid with virtualization for performance
    function displayIcons(resetDisplayCount = true) {
        console.log('Displaying icons');
        const grid = document.getElementById('iconGrid');
        const searchTerm = document.getElementById('searchInput').value.trim();
        const selectedSources = Array.from(document.querySelectorAll('input[name="source"]:checked')).map(cb => cb.value);
        
        console.log('Search term:', searchTerm);
        console.log('Selected sources:', selectedSources);
        
        // Reset display count when performing a new search
        if (resetDisplayCount) {
            currentDisplayCount = 500;
            grid.innerHTML = '';
        }
        
        // Always remove existing button containers
        const existingButtonContainer = document.querySelector('.button-container');
        if (existingButtonContainer) {
            existingButtonContainer.remove();
        }
        
        let filteredIcons = icons;
        
        // Apply search filter if search term exists
        if (searchTerm) {
            console.log('Performing search for:', searchTerm);
            
            // Use optimized search for better performance
            filteredIcons = performOptimizedSearch(searchTerm);
            console.log('Search results:', filteredIcons.length);
        }
        
        // Apply source filter
        filteredIcons = filteredIcons.filter(icon => selectedSources.includes(icon.source));
        console.log('Filtered icons after source filter:', filteredIcons.length);
        
        // Limit the number of icons displayed for performance
        const displayIconsList = filteredIcons.slice(0, currentDisplayCount);
        
        if (filteredIcons.length > currentDisplayCount) {
            console.log(`Showing first ${currentDisplayCount} of ${filteredIcons.length} results`);
        }
        
        // Use DocumentFragment for better performance
        const fragment = document.createDocumentFragment();
        
        // If we're loading more, we need to add only the new icons
        const startIndex = resetDisplayCount ? 0 : currentDisplayCount - 500;
        const iconsToAdd = displayIconsList.slice(startIndex);
        
        iconsToAdd.forEach(icon => {
            const iconElement = document.createElement('div');
            iconElement.className = `icon-card ${selectedIcons.has(icon.path) ? 'selected' : ''}`;
            iconElement.dataset.path = icon.path;
            iconElement.dataset.name = icon.name;
            iconElement.dataset.tags = icon.tags ? JSON.stringify(icon.tags) : '';
            iconElement.innerHTML = `
                <img src="${icon.path}" alt="${icon.name}">
            `;
            
            // Add tooltip functionality
            iconElement.addEventListener('mouseenter', showTooltip);
            iconElement.addEventListener('mouseleave', hideTooltip);
            
            fragment.appendChild(iconElement);
        });
        
        grid.appendChild(fragment);
        
        // Add "Load more" button if there are more results
        if (filteredIcons.length > currentDisplayCount) {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'button-container';
            buttonContainer.style.display = 'flex';
            buttonContainer.style.justifyContent = 'center';
            buttonContainer.style.gap = '1rem';
            buttonContainer.style.marginTop = '1rem';
            
            const loadMoreBtn = document.createElement('button');
            loadMoreBtn.className = 'load-more-btn';
            loadMoreBtn.textContent = `Load More (${Math.min(500, filteredIcons.length - currentDisplayCount)} more)`;
            loadMoreBtn.addEventListener('click', () => {
                currentDisplayCount += 500;
                displayIcons(false); // Don't reset display count
            });
            
            const loadAllBtn = document.createElement('button');
            loadAllBtn.className = 'load-all-btn';
            loadAllBtn.textContent = `Load All (${filteredIcons.length - currentDisplayCount} remaining)`;
            loadAllBtn.addEventListener('click', () => {
                currentDisplayCount = filteredIcons.length;
                displayIcons(false); // Don't reset display count
            });
            
            buttonContainer.appendChild(loadMoreBtn);
            buttonContainer.appendChild(loadAllBtn);
            
            // Add buttons after the grid, not inside it
            const main = document.querySelector('main');
            main.appendChild(buttonContainer);
        }
        
        // Update results count
        updateResultsCount(filteredIcons.length);
    }

    // Tooltip functionality
    function showTooltip(event) {
        const card = event.currentTarget;
        const name = card.dataset.name;
        const tags = card.dataset.tags ? JSON.parse(card.dataset.tags) : [];
        
        // Remove any existing tooltip
        const existingTooltip = document.querySelector('.icon-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'icon-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-name">${name}</div>
            ${tags.length > 0 ? `<div class="tooltip-tags">${tags.map(tag => `<span class="tooltip-tag">${tag}</span>`).join('')}</div>` : ''}
        `;
        
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = card.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        
        let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
        let top = rect.bottom + 10;
        
        // Adjust if tooltip goes off screen
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }
        if (top + tooltipRect.height > window.innerHeight - 10) {
            top = rect.top - tooltipRect.height - 10;
        }
        
        tooltip.style.left = left + 'px';
        tooltip.style.top = top + 'px';
    }

    function hideTooltip() {
        const tooltip = document.querySelector('.icon-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    // Update results count display
    function updateResultsCount(count) {
        const totalCount = icons.length;
        const searchInput = document.getElementById('searchInput');
        const searchTerm = searchInput.value.trim();
        
        if (searchTerm) {
            searchInput.placeholder = `Search icons... (${count} of ${totalCount} results)`;
        } else {
            searchInput.placeholder = `Search icons...`;
        }
    }

    // Search functionality with optimized debouncing
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.trim();
        
        // Don't search for very short terms to improve performance
        if (searchTerm.length < 2 && searchTerm.length > 0) {
            return;
        }
        
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            displayIcons();
        }, 200); // Reduced from 300ms to 200ms for better responsiveness
    });

    // Source filter functionality
    sourceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', displayIcons);
    });

    // Cart functionality
    const cartBtn = document.getElementById('cartBtn');
    const cartContent = document.querySelector('.cart-content');
    const cartItems = document.querySelector('.cart-items');
    const cartCount = document.querySelector('.cart-count');

    console.log('Cart elements:', { cartBtn, cartContent, cartItems, cartCount, downloadBtn });

    // Toggle cart dropdown
    cartBtn.addEventListener('click', (e) => {
        console.log('Cart button clicked');
        e.stopPropagation();
        cartContent.classList.toggle('show');
    });

    // Close cart when clicking outside
    document.addEventListener('click', (e) => {
        if (!cartContent.contains(e.target) && !cartBtn.contains(e.target)) {
            cartContent.classList.remove('show');
        }
    });

    // Prevent cart from closing when clicking inside
    cartContent.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    // Update cart display
    function updateCart() {
        console.log('Updating cart, selected icons:', selectedIcons);
        cartItems.innerHTML = '';
        selectedIcons.forEach(path => {
            const icon = icons.find(i => i.path === path);
            if (icon) {
                const item = document.createElement('div');
                item.className = 'cart-item';
                item.innerHTML = `
                    <img src="${icon.path}" alt="${icon.name}">
                    <span class="item-name">${icon.name}</span>
                    <button class="remove-btn" data-path="${icon.path}">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                cartItems.appendChild(item);
            }
        });
        
        // Update cart count and button states
        const count = selectedIcons.size;
        console.log('Cart count:', count);
        cartCount.textContent = count;
        
        // Enable/disable cart button based on selection count
        if (count > 0) {
            console.log('Enabling cart button');
            cartBtn.removeAttribute('disabled');
        } else {
            console.log('Disabling cart button');
            cartBtn.setAttribute('disabled', 'disabled');
            cartContent.classList.remove('show');
        }
        
        // Enable/disable download button
        downloadBtn.disabled = count === 0;
    }

    // Handle icon selection
    document.addEventListener('click', (e) => {
        const card = e.target.closest('.icon-card');
        if (card) {
            console.log('Card clicked:', card.dataset);
            const path = card.dataset.path;
            const name = card.dataset.name;
            
            if (selectedIcons.has(path)) {
                console.log('Removing from cart:', path);
                selectedIcons.delete(path);
                card.classList.remove('selected');
            } else {
                console.log('Adding to cart:', path);
                selectedIcons.add(path);
                card.classList.add('selected');
            }
            
            updateCart();
        }
    });

    // Handle remove from cart
    cartItems.addEventListener('click', (e) => {
        if (e.target.closest('.remove-btn')) {
            const btn = e.target.closest('.remove-btn');
            const path = btn.dataset.path;
            console.log('Removing from cart via button:', path);
            selectedIcons.delete(path);
            
            // Update the card in the grid
            const card = document.querySelector(`.icon-card[data-path="${path}"]`);
            if (card) {
                card.classList.remove('selected');
            }
            
            updateCart();
        }
    });

    // Download functionality
    downloadBtn.addEventListener('click', async () => {
        console.log('Downloading selected icons:', selectedIcons);
        const zip = new JSZip();
        
        // Track used names to handle duplicates
        const usedNames = new Map();
        
        // Add each selected icon to the zip
        for (const path of selectedIcons) {
            try {
                const response = await fetch(path);
                const blob = await response.blob();
                
                // Find the icon data to get the name
                const icon = icons.find(i => i.path === path);
                if (!icon) {
                    console.error(`Icon not found for path: ${path}`);
                    continue;
                }
                
                // Get the file extension from the original path
                const originalFilename = path.split('/').pop();
                const fileExtension = originalFilename.split('.').pop();
                
                // Create filename from icon name
                let filename = icon.name;
                
                // Handle duplicates by appending incrementing numbers
                if (usedNames.has(filename)) {
                    const count = usedNames.get(filename) + 1;
                    usedNames.set(filename, count);
                    filename = `${icon.name} (${count})`;
                } else {
                    usedNames.set(filename, 1);
                }
                
                // Add file extension
                filename = `${filename}.${fileExtension}`;
                
                // Sanitize filename (remove invalid characters)
                filename = filename.replace(/[<>:"/\\|?*]/g, '_');
                
                zip.file(filename, blob);
            } catch (error) {
                console.error(`Error adding ${path} to zip:`, error);
            }
        }
        
        // Generate and download the zip file
        zip.generateAsync({type: 'blob'})
            .then(content => {
                const link = document.createElement('a');
                link.href = URL.createObjectURL(content);
                link.download = 'selected-icons.zip';
                link.click();
            });
    });
}); 