console.log('premium_header.js chargé');
// --- Sidebar premium ---
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar
    const openMenuBtn = document.getElementById('openMenuBtn');
    const sidebar = document.getElementById('premiumSidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    // Nouvelle structure : catégories et sous-menus dans des conteneurs séparés
    const categories = sidebar ? sidebar.querySelectorAll('.sidebar-categories .menu-category') : [];
    const allSubmenus = sidebar ? sidebar.querySelectorAll('.sidebar-submenus .menu-submenu') : [];
    const submenuTabPanel = document.getElementById('submenuTabPanel');
    const toggleSubmenuTab = document.getElementById('toggleSubmenuTab');
    let submenuTabOpen = true;
    if(openMenuBtn && sidebar) {
        openMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.add('show');
        });
        if(closeSidebar) {
            closeSidebar.addEventListener('click', function(e) {
                sidebar.classList.remove('show');
            });
        }
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && e.target !== openMenuBtn) {
                sidebar.classList.remove('show');
            }
        });
        // Gestion des sous-menus par data-submenu (nouvelle colonne)
        categories.forEach(cat => {
            cat.addEventListener('mouseenter', function() {
                console.log('Survol catégorie', cat, cat.getAttribute('data-submenu'));
                categories.forEach(c => c.classList.remove('active'));
                cat.classList.add('active');
                // Masquer tous les sous-menus
                allSubmenus.forEach(sm => sm.classList.remove('active'));
                const submenuId = cat.getAttribute('data-submenu');
                if(submenuId) {
                    const submenu = document.getElementById(submenuId);
                    if(submenu) {
                        submenu.classList.add('active');
                        console.log('Sous-menu activé', submenu);
                    }
                    // Afficher le bouton toggle si un sous-menu est actif
                    if(toggleSubmenuTab) toggleSubmenuTab.style.display = '';
                    if(submenuTabPanel) {
                        submenuTabPanel.style.transform = 'translateX(0)';
                        submenuTabOpen = true;
                        if(toggleSubmenuTab) toggleSubmenuTab.innerHTML = '<i class="fas fa-chevron-right"></i>';
                    }
                } else {
                    if(toggleSubmenuTab) toggleSubmenuTab.style.display = 'none';
                    if(submenuTabPanel) submenuTabPanel.style.transform = 'translateX(0)';
                }
            });
        });
        // Rétractation du panneau sous-menu
        if(toggleSubmenuTab && submenuTabPanel) {
            toggleSubmenuTab.addEventListener('click', function() {
                submenuTabOpen = !submenuTabOpen;
                if(submenuTabOpen) {
                    submenuTabPanel.style.transform = 'translateX(0)';
                    toggleSubmenuTab.innerHTML = '<i class="fas fa-chevron-right"></i>';
                } else {
                    submenuTabPanel.style.transform = 'translateX(100%)';
                    toggleSubmenuTab.innerHTML = '<i class="fas fa-chevron-left"></i>';
                }
            });
        }
        // Ferme les sous-menus quand la souris quitte la sidebar
        sidebar.addEventListener('mouseleave', function() {
            categories.forEach(c => c.classList.remove('active'));
            allSubmenus.forEach(sm => sm.classList.remove('active'));
            if(toggleSubmenuTab) toggleSubmenuTab.style.display = 'none';
            if(submenuTabPanel) submenuTabPanel.style.transform = 'translateX(0)';
            submenuTabOpen = true;
        });
    }
    // --- Sous-entête rétractable ---
    const subheader = document.getElementById('premium-subheader');
    const toggleSubheader = document.getElementById('toggleSubheader');
    let subheaderOpen = true;
    if(subheader && toggleSubheader) {
        toggleSubheader.addEventListener('click',function(){
            subheaderOpen = !subheaderOpen;
            if(subheaderOpen){
                subheader.style.maxHeight = '60px';
                toggleSubheader.innerHTML = '<i class="fas fa-chevron-up"></i>';
            }else{
                subheader.style.maxHeight = '0';
                toggleSubheader.innerHTML = '<i class="fas fa-chevron-down"></i>';
            }
        });
    }
});
