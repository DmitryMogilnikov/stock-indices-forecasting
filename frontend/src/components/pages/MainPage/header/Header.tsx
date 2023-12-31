import React from "react";
import "./../../../../styles/Header.model.scss";
import "./../../../../styles/variables.scss";

function Header() {
    return (
        <header className="Header">
            <div className="Header__content">
                <h1 className="NoSelect">Прогнозирование фондовых индексов</h1>
            </div>
        </header>
    )
}

export default Header
