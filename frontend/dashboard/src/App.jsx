import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import SelectionPage from "./pages/selectionPage/selectionPage";
import Upload from "./pages/upload/upload";

function App() {
  return (
    <>
      <div className="App">
        <ToastContainer
          position="bottom-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        ></ToastContainer>
        <Router>
          <Routes>
            <Route path="/" element={<SelectionPage />}></Route>
            <Route path="/upload" element={<Upload />}></Route>
          </Routes>
        </Router>
      </div>
    </>
  );
}

export default App;
