import { BACKENDADDRESS } from "./address";

export const callAPI = async (method, formData, APIName) => {
  try {
    const response = await fetch(BACKENDADDRESS + APIName, {
      method: method,
      body: formData,
    });
    return response;
  } catch (error) {
    console.error("Error during file upload:", error);
  }
};
