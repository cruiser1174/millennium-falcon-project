/** @jsxImportSource @emotion/react */
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
        <div css={{margin: '0.5rem 4rem'}}>
            <h3>Upload a new scenario</h3>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileUpload}/>
                <button type="submit">Upload</button>
            </form>
        </div>
    );
}