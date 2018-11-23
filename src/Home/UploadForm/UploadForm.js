import React, {Component } from 'react'
import { FilePond, File } from 'react-filepond';
import 'filepond/dist/filepond.min.css';

class UploadForm extends Component {
    constructor(props) {
        super(props);

        this.state = {
            // Set initial files
            files: []
        };
    }

    componentDidUpdate = (prevProps, prevState) => {
        console.log(this.state);
    }
    
    render() {
        return (
            <div>
                <FilePond
                    server="/upload"
                    onupdatefiles={(fileItems) => { 
                        this.setState({ files: fileItems.map(fileItem => fileItem.file) }); }}>
                    
                    {this.state.files.map(file => (
                        <File key={file} src={file} origin="local" />
                    ))}
                </FilePond>


                <div className="ui placeholder segment">
                    <div className="ui icon header">
                        <i className="archive icon"/>
                        <p>Upload the zip file with the student's assignment submission.</p>
                        <p>Make sure it contains files [a1_p1.py, a1_p2.py ..].</p>
                    </div>
                </div>
            </div>
        )
    }
}

{/*<form method="POST"  action="/test">

      </form>*/
}

export default UploadForm