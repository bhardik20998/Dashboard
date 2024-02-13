import React, { useRef } from "react";
import "./upload.css";
import { callAPI } from "../../constants/functions";
import { APIS } from "../../constants/address";
const Upload = () => {
  const fileInputRef = useRef(null);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log(file);
    onFileUpload(file);
  };

  const onFileUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await callAPI("POST", formData, APIS.UPLOAD);
    console.log(response);
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="upload-page-body">
      <div className="upload-page-background">
        <div className="upload-page-shape"></div>
        <div className="upload-page-shape"></div>
      </div>
      <div className="upload-page-form">
        <h3>Upload Excel File</h3>

        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx, .xls"
          style={{
            display: "none",
          }}
          onChange={handleFileChange}
          id="fileInput"
        />
        <label htmlFor="fileInput">
          <button className="upload-page-button" onClick={handleButtonClick}>
            Upload Excel File
          </button>
        </label>
      </div>
    </div>
  );
};
export default Upload;
