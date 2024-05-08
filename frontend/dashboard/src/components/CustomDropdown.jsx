import { useState } from "react";

export default function CustomDropdown(props) {
  const {
    row,
    dropdownKey,
    dropdownValues,
    handleDropdownChange,
    header,
    state,
  } = props;
  // console.log(header);
  const [showList, setShowList] = useState(false);

  return (
    <div
      id={dropdownKey}
      style={{
        backgroundColor: (() => {
          switch (dropdownValues[dropdownKey]) {
            case "AR":
              return "#ffcccb"; // Set background color for option1
            case "AA":
              return "#7FFF00"; // Set background color for option2
            case "L1":
              return " #aaffaa"; // Set background color for option2
            case "L2":
              return "#FFFF00"; // Set background color for option3
            case "L3":
              return "#ccddff"; // Set background color for option4
            case "L4":
              return "#FFDAB9"; // Set background color for option4

            default:
              return "#e5f7ff"; // Set default background color
          }
        })(),
        color: "#0077cc",
        position: "relative", // Set your desired text color for the dropdown
      }}
    >
      <button
        style={{ background: "none", outline: "none", border: "none" }}
        onClick={() => setShowList((v) => !v)}
      >
        {dropdownValues[dropdownKey] || ""}
      </button>
      {showList && (
        <div
          style={{
            position: "absolute",
            top: "1.5em",
            background: "#fff",
            display: "grid",
            zIndex: "999",
            padding: "6px",
            gap: "0.5em",
          }}
        >
          {["AA", "L1", "L2", "L3", "L4", "AR"].map((option) => {
            if (
              (option === "AR" &&
                dropdownValues[dropdownKey] === "AA" &&
                !state) ||
              (option === "AA" &&
                dropdownValues[dropdownKey] === "AR" &&
                !state)
            ) {
              return null; // Exclude the option from rendering
            }

            return (
              <button
                style={{
                  background: "none",
                  outline: "none",
                  border: "none",
                  padding: "4px 6px",
                }}
                onClick={() => {
                  handleDropdownChange(row["CIBIL_Bucket"], header, option);
                  setShowList(false);
                }}
              >
                {option}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
