import React from "react";
import "./sideBar.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { sidebarItems } from "../../constants/constants";
const Sidebar = ({ onItemClick }) => {
  const sidebarItem = sidebarItems;

  return (
    <div className="beautiful-sidebar">
      <nav>
        {sidebarItem.map((item, index) => (
          <a key={index} onClick={() => onItemClick(item)}>
            <span>{item.title}</span>
          </a>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
