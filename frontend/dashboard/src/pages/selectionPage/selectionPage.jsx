import React from "react";
import "./selectionPage.css";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../constants/paths";

const SelectionPage = () => {
  const navigate = useNavigate();
  const clickHandler = (e) => {
    if (e.target.value == "GT") {
      localStorage.setItem("mode", "GT");
    } else {
      localStorage.setItem("mode", "LT");
    }
    navigate(PATHS.UPLOAD);
  };
  return (
    <div className="selection-page-body">
      <div className="selection-page-background">
        <div className="selection-page-shape"></div>
        <div className="selection-page-shape"></div>
      </div>
      <div className="selection-page-form">
        <h3>Select Condition!</h3>

        <button
          className="selection-page-button"
          value="GT"
          onClick={clickHandler}
        >
          GT-60
        </button>
        <button
          className="selection-page-button"
          value="LT"
          onClick={clickHandler}
        >
          LT-60
        </button>
      </div>
    </div>
  );
};

export default SelectionPage;
