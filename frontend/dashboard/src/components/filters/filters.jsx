import React, { useEffect, useState } from "react";
import "./filters.css";
import { filterItems } from "../../constants/constants";

const Filters = ({ filterValues, checkedItems, setCheckedItems }) => {
  const handleCheckboxChange = (heading, item) => {
    setCheckedItems((prevCheckedItems) => ({
      ...prevCheckedItems,
      [heading]: {
        ...(prevCheckedItems[heading] || {}),
        [item]: !prevCheckedItems[heading]?.[item],
      },
    }));
  };
  console.log();

  const handleCheckBoxAllChange = (heading, isChecked) => {
    setCheckedItems((prevCheckedItems) => {
      const updatedCheckedItems = {};

      filterValues[heading]?.forEach((item) => {
        updatedCheckedItems[heading] = {
          ...(updatedCheckedItems[heading] || {}),
          [item]: isChecked,
        };
      });

      return {
        ...prevCheckedItems,
        ...updatedCheckedItems,
      };
    });
  };

  if (!filterValues) {
    return <div></div>;
  } else {
    return (
      <div className="filters-main">
        <h2 className="filters-heading">Filters</h2>
        {Object.keys(filterValues)?.map((heading) => {
          return (
            <div key={heading} className="scrollable-div">
              <span className="filters-subheaders">
                <input
                  type="checkbox"
                  onChange={(e) => {
                    handleCheckBoxAllChange(heading, e.target.checked);
                  }}
                  defaultChecked
                ></input>{" "}
                {filterItems?.find((item) => item?.id === heading)?.value}{" "}
              </span>
              <ul className="filters-ul">
                {filterValues[heading]?.map((item) => {
                  return (
                    <li key={item}>
                      <label>
                        <input
                          checked={checkedItems[heading]?.[item] || false}
                          type="checkbox"
                          //   checked={checkedItems[item] || false}
                          onChange={() => handleCheckboxChange(heading, item)}
                        />
                        {item}
                      </label>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>
    );
  }
};

export default Filters;
