document.addEventListener("DOMContentLoaded", function() {
    const toggleMenus = document.querySelectorAll(".toggle-menu, .toggle-menu2, .toggle-menu3, .toggle-menu4");
    const submenus = document.querySelectorAll(" .rep, .bus ");
   
    toggleMenus.forEach(menu => {
        menu.addEventListener("click", function(e) {
            e.preventDefault();

            //para cerrar todos los submenus
            toggleMenus.forEach(otherMenu => {
                const otherSubmenu = otherMenu.nextElementSibling;
                if (otherSubmenu && otherSubmenu !== menu.nextElementSibling) {
                    otherSubmenu.style.display = "none";
                }
            });

            //alterar el submenu actual
            const submenu = menu.nextElementSibling;
            submenu.style.display = (submenu.style.display === "block") ? "none" : "block";
        });
    });

    submenus.forEach(menu => {//abrir submenus con hover (mouseover)
        menu.addEventListener("mouseover", function(e) {
            e.preventDefault();

            //para cerrar todos los submenus
            submenus.forEach(otherMenu => {
                const otherSubmenu = otherMenu.nextElementSibling;
                if (otherSubmenu && otherSubmenu !== menu.nextElementSibling) {
                    otherSubmenu.style.display = "none";
                }
            
            });
            //alterar el submenu actual
            const submenu = menu.nextElementSibling;
            submenu.style.display = (submenu.style.display === "block") ? "none" : "block";
          
            
        });
    });

    //evento para que cierre los submenus al hacer click fuera de ellos
    document.addEventListener("click", function(e) {
        // Si el clic no fue en un menu o submenu, cierra todos los submenus
        if (!e.target.closest(".toggle-menu") && !e.target.closest(".toggle-menu2") && !e.target.closest(".toggle-menu3") && !e.target.closest(".toggle-menu4") && !e.target.closest(".resp") && !e.target.closest(".bus")) {
            toggleMenus.forEach(menu => {
                const submenu = menu.nextElementSibling;
                if (submenu) submenu.style.display = "none";
            });
            //cierra los submenus que se quedaron abiertos al dar click fuera de ellos 
            submenus.forEach(menu => {
                const submenu = menu.nextElementSibling;
                if (submenu) submenu.style.display = "none";
            });
        }
        
    });
});
