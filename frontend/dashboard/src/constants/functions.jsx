import { BACKENDADDRESS } from "./address";

export const callAPI = async (method, formData, APIName, signal) => {
  try {
    const fetchOptions = {
      method: method,
      body: formData,
    };
    if (signal) {
      fetchOptions["signal"] = signal;
    }
    const response = await fetch(BACKENDADDRESS + APIName, fetchOptions);
    return response;
  } catch (error) {
    console.error("Error:", error);
  }
};
