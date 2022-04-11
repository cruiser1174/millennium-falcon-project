import React from "react";

export function SubmitScenarioForm(props) {
    function handleFileUpload(event) {
        props.handleUpload(event.target.files[0]);
      };

      function handleSubmit(event) {
          event.preventDefault();
          try {
            props.handleSubmit(props.file);
          } catch(e) {
              alert(e);
          };
      }
      
    
    return (
        <div className="upload-file-container">
            <h3 id="upload-form-caption">Upload a new scenario</h3>
            <form className="upload-form" onSubmit={handleSubmit}>
                <input className="upload-input" type="file" onChange={handleFileUpload}/>
                <button className="submit-button" type="submit">Upload Scenario</button>
            </form>
        </div>
    );
}