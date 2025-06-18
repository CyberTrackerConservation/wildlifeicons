document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const iconGrid = document.getElementById('iconGrid');
    const downloadBtn = document.getElementById('downloadBtn');
    const styleCheckboxes = document.querySelectorAll('input[name="style"]');
    const dropdownBtn = document.querySelector('.style-dropdown-btn');
    const dropdownContent = document.querySelector('.style-dropdown-content');
    let icons = [];
    let selectedIcons = new Set();

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
            icons = data.icons.map(icon => ({
                ...icon,
                path: `icons/${icon.filename}`
            }));
            console.log('Processed icons:', icons);
            displayIcons();
        })
        .catch(error => {
            console.error('Error loading icons:', error);
        });

    // Display icons in the grid
    function displayIcons() {
        console.log('Displaying icons');
        const grid = document.getElementById('iconGrid');
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const selectedStyles = Array.from(document.querySelectorAll('input[name="style"]:checked')).map(cb => cb.value);
        
        grid.innerHTML = '';
        
        icons.forEach(icon => {
            const matchesSearch = icon.name.toLowerCase().includes(searchTerm) || 
                                (icon.keywords && icon.keywords.some(keyword => keyword.toLowerCase().includes(searchTerm)));
            
            if (matchesSearch && selectedStyles.includes(icon.style)) {
                const iconElement = document.createElement('div');
                iconElement.className = `icon-card ${selectedIcons.has(icon.path) ? 'selected' : ''}`;
                iconElement.dataset.path = icon.path;
                iconElement.dataset.name = icon.name;
                iconElement.innerHTML = `
                    <img src="${icon.path}" alt="${icon.name}">
                    <div class="icon-info">
                        <span class="icon-name">${icon.name}</span>
                    </div>
                    <div class="select-indicator">
                        <i class="fas ${selectedIcons.has(icon.path) ? 'fa-check' : 'fa-plus'}"></i>
                    </div>
                `;
                grid.appendChild(iconElement);
            }
        });
    }

    // Search functionality
    searchInput.addEventListener('input', displayIcons);

    // Style filter functionality
    styleCheckboxes.forEach(checkbox => {
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
                card.querySelector('.select-indicator i').className = 'fas fa-plus';
            } else {
                console.log('Adding to cart:', path);
                selectedIcons.add(path);
                card.classList.add('selected');
                card.querySelector('.select-indicator i').className = 'fas fa-check';
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
                card.querySelector('.select-indicator i').className = 'fas fa-plus';
            }
            
            updateCart();
        }
    });

    // Download functionality
    downloadBtn.addEventListener('click', async () => {
        console.log('Downloading selected icons:', selectedIcons);
        const zip = new JSZip();
        
        // Add each selected icon to the zip
        for (const path of selectedIcons) {
            try {
                const response = await fetch(path);
                const blob = await response.blob();
                const filename = path.split('/').pop();
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