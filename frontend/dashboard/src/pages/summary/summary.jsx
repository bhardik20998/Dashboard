import React, { useEffect, useState } from "react";
import { callAPI } from "../../constants/functions";
import { APIS } from "../../constants/address";
import "./summary.css";
import Sidebar from "../../components/sideBar/sideBar";
import Filters from "../../components/filters/filters";
import { KPIsItems, sidebarItems } from "../../constants/constants";
import CustomDropdown from "../../components/CustomDropdown";
import * as XLSX from "xlsx";

const Summary = () => {
  const [totalAppData, setTotalAppData] = useState();
  const [headers, setHeaders] = useState();
  const [selection, setSelection] = useState(sidebarItems[0]);
  const [filterValues, setFilterValues] = useState();
  const [checkedItems, setCheckedItems] = useState({});
  const [KPIs, setKPIs] = useState();
  const [KPIsHeaders, setKPIsHeaders] = useState([
    "Bad Definations",
    "AR",
    "L4",
    "L3",
    "L2",
    "L1",
    "AA",
  ]);
  const [loader, setLoader] = useState(true);

  const [dropdownValues, setDropdownValues] = useState({});
  function allValuesTrue(obj) {
    for (const key in obj) {
      if (typeof obj[key] === "object") {
        for (const innerKey in obj[key]) {
          if (!obj[key][innerKey]) {
            return false; // If any inner value is false, return false
          }
        }
      } else {
        if (!obj[key]) {
          return false; // If any value is false, return false
        }
      }
    }
    return true; // If all values are true, return true
  }

  useEffect(() => {
    callAPI(
      "POST",
      JSON.stringify({
        Selection: selection.id,
        Filters: checkedItems,
        dropDownDict: dropdownValues,
        changed: "Selection",
      }),
      APIS.SUMMARY
    ).then((res) => {
      res.json().then((res) => {
        if (res) {
          // setDropdownValues(res.dropDownDict);
          setTotalAppData(JSON.parse(res.total_applications));
          setHeaders(Object.keys(JSON.parse(res.total_applications)[0]));
          setFilterValues(res.filter_values);

          setKPIs(JSON.parse(res["KPIs Table"]));

          const initialCheckedItems = {};
          Object.keys(res.filter_values).forEach((heading) => {
            initialCheckedItems[heading] = {};
            if (res.filter_values[heading]) {
              res.filter_values[heading].forEach((item) => {
                initialCheckedItems[heading][item] = true;
              });
            }
          });
          setCheckedItems(initialCheckedItems);
        }
      });
    });
  }, [selection]);

  useEffect(() => {
    setLoader(true);
    if (Object.keys(checkedItems).length) {
      callAPI(
        "POST",
        JSON.stringify({
          Selection: selection.id,
          Filters: checkedItems,
          dropDownDict: dropdownValues,
          changed: "checkedItems",
        }),
        APIS.SUMMARY
      ).then((res) => {
        if (res) {
          setLoader(false);
          res.json().then((res) => {
            setTotalAppData(JSON.parse(res.total_applications));
            setHeaders(
              Object.keys(JSON.parse(res.total_applications)?.[0] || {})
            );
            setFilterValues(res.filter_values);

            setDropdownValues(res.dropDownDict);

            setKPIs(JSON.parse(res["KPIs Table"]));
          });
        }
      });
    }
  }, [checkedItems]);
  useEffect(() => {
    console.log(dropdownValues);
    if (Object.keys(dropdownValues).length) {
      callAPI(
        "POST",
        JSON.stringify({
          Selection: selection.id,
          Filters: checkedItems,
          dropDownDict: dropdownValues,
          changed: "dropdownValues",
        }),
        APIS.SUMMARY
      ).then((res) => {
        if (res) {
          res.json().then((res) => {
            setTotalAppData(JSON.parse(res.total_applications));
            setHeaders(Object.keys(JSON.parse(res.total_applications)[0]));
            setFilterValues(res.filter_values);

            setKPIs(JSON.parse(res["KPIs Table"]));
          });
        }
      });
    }
  }, [dropdownValues]);

  // console.log(headers);
  useEffect(() => {
    if (totalAppData == undefined) {
      setLoader(true);
    } else {
      setLoader(false);
    }
  }, [totalAppData]);

  const exportToExcel = async () => {
    try {
      const response = await callAPI("POST", {}, APIS.DOWNLOADDATA);
      const data = await response.json();
      // console.log(JSON.parse(data.data));

      // Download data to Excel
      const ws = XLSX.utils.json_to_sheet(JSON.parse(data.data));
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      XLSX.writeFile(wb, "Results.xlsx");
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleItemClick = (item) => {
    setSelection(item);
  };
  const handleDropdownChange = (scoreBucket, header, selectedValue) => {
    // Update the state with the selected value
    setDropdownValues((prevValues) => ({
      ...prevValues,
      [scoreBucket + "_" + header]: selectedValue,
    }));
  };
  return (
    <div>
      {loader ? (
        <div className="loader-body">
          <div className="loader"></div>
        </div>
      ) : (
        <div className="summary-body">
          <div>
            <Sidebar onItemClick={handleItemClick} />
          </div>

          <div className="summary-table-wrapper">
            <div>
              <h2 className="summary-h2"> {selection?.title}</h2>
              <table className="fl-table">
                <thead>
                  <tr>
                    <th style={{ background: " rgba(71, 147, 227, 1)" }}></th>
                    <th
                      style={{ background: "black" }}
                      colSpan={Object.keys(totalAppData).length - 1}
                    >
                      In-House Scores
                    </th>

                    <th style={{ background: " rgba(71, 147, 227, 1)" }}></th>
                  </tr>
                  <tr>
                    {headers?.map((header, index) => (
                      <th key={index}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {totalAppData?.map((row, rowIndex) => {
                    return (
                      <tr key={rowIndex}>
                        {headers?.map((header, headerIndex) => (
                          <td key={headerIndex}>{row[header]}</td>
                        ))}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            <div className="summary-bottom-tables-wrapper">
              <div>
                <h4 className="summary-h2">Decision Matrix</h4>
                <table className="fl-table1">
                  <thead>
                    <tr>
                      <th style={{ background: " rgba(71, 147, 227, 1)" }}></th>
                      <th
                        style={{ background: "black" }}
                        colSpan={Object.keys(totalAppData).length - 1}
                      >
                        In-House Scores
                      </th>
                    </tr>
                    <tr>
                      {headers?.map((header, index) => {
                        if (header != "Total") {
                          return <th key={index}>{header}</th>;
                        }
                      })}
                    </tr>
                  </thead>
                  <tbody>
                    {totalAppData?.map((row, rowIndex) => {
                      if (row["CIBIL_Bucket"] != "Total") {
                        return (
                          <tr key={rowIndex}>
                            {headers?.map((header, headerIndex) => {
                              if (headerIndex == 0) {
                                return <td key={headerIndex}>{row[header]}</td>;
                              } else if (header == "Total") {
                              } else {
                                const dropdownKey =
                                  row["CIBIL_Bucket"] + "_" + header;
                                // console.log(row);
                                return (
                                  <td key={headerIndex}>
                                    <CustomDropdown
                                      header={header}
                                      row={row}
                                      dropdownKey={dropdownKey}
                                      dropdownValues={dropdownValues}
                                      handleDropdownChange={
                                        handleDropdownChange
                                      }
                                      state={allValuesTrue(checkedItems)}
                                    />
                                  </td>
                                );
                              }
                            })}
                          </tr>
                        );
                      }
                    })}
                  </tbody>
                </table>
              </div>
              <div>
                <h4 className="summary-h2">KPIs</h4>
                <table className="fl-table1">
                  <thead>
                    <tr>
                      {KPIsHeaders?.map((header, index) => {
                        return <th key={index}>{header}</th>;
                      })}
                    </tr>
                  </thead>
                  <tbody>
                    {KPIs?.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {KPIsHeaders?.map((header, headerIndex) => {
                          console.log(KPIs);
                          return (
                            <td key={headerIndex}>
                              {headerIndex == 0 ? (
                                <>
                                  {
                                    KPIsItems?.find(
                                      (item) => item.id == row[header]
                                    ).title
                                  }
                                  (%)
                                </>
                              ) : (
                                <> {row[header]}</>
                              )}{" "}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    paddingTop: "10px",
                  }}
                >
                  <button className="button-55" onClick={exportToExcel}>
                    Download Excel
                  </button>
                </div>
              </div>
            </div>
          </div>
          <Filters
            filterValues={filterValues}
            checkedItems={checkedItems}
            setCheckedItems={setCheckedItems}
          />
        </div>
      )}
    </div>
  );
};
export default Summary;
