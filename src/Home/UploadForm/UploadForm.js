import React from 'react'
import axios, { post } from 'axios';

class UploadForm extends React.Component {
  constructor(props) {
    super(props);
    this.state ={
      file:null
    }
  }

  onFormSubmit = (e) => {
    e.preventDefault(); // Stop form submit
    this.fileUpload(this.state.file).then((response)=>{
      console.log(response.data);
    })
  };

  onChange = (e) => {
    this.setState({file:e.target.files[0]})
  };

  fileUpload = (file) => {
    const url = 'localhost:5000/file-upload';
    const formData = new FormData();
    formData.append('file',file);
    const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    };

    return post(url, formData,config)
  };

  render() {
    return (
      <form onSubmit={this.onFormSubmit}>
        <div className="ui placeholder segment">
          <div className="ui icon header">
            <i className="archive icon" />
            <p>Upload the zip file with the student's assignment submission.</p>
            <p>Make sure it contains files [a1_p1.py, a1_p2.py ..].</p>
          </div>
          <div className="inline">
            <label htmlFor="file" className="ui icon button">
              <i className="file archive icon" />
            </label>
            <input className="ui primary button" type="file" name="file" id="file" style={{display:"none"}} />
          </div>
        </div>

        <input type="file" onChange={this.onChange} />
        <button type="submit">Upload</button>
      </form>
    )
  }
}



export default UploadForm