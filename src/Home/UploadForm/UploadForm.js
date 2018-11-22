import React from 'react'
import axios, {post} from 'axios';

class UploadForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            file: null
        }
    }

    onFormSubmit = (e) => {
        e.preventDefault(); // Stop form submit
        this
            .fileUpload(this.state.file)
            .then((response) => {
                console.log(response.data);
            })
    };

    onChange = (e) => {
        this.setState({file: e.target.files[0]})
    };

    fileUpload = (file) => {
        const url = "/upload";
        const formData = new FormData();
        formData.append('file', file);
        const config = {
            headers: {
                'content-type': 'multipart/form-data'
            }
        };

        return post(url, formData, config)
    };

    test = () => {
        const url = "/test";
        const formData = new FormData();
        formData.append('data', "hello");

        const config = {
            headers: {
                'content-type': 'application/json' // 'multipart/form-data'
            }
        };

        return post(url, formData)
    };

    render() {
        return (
            <form method="post" encType="multipart/form-data" action="/upload">
                <div className="ui placeholder segment">
                    <div className="ui icon header">
                        <i className="archive icon"/>
                        <p>Upload the zip file with the student's assignment submission.</p>
                        <p>Make sure it contains files [a1_p1.py, a1_p2.py ..].</p>
                    </div>
                    <div className="inline">
                        <input type="submit" className="ui primary button"/>

                        <label htmlFor="file" className="ui icon button">
                            <i className="file archive icon"/>
                            Upload zip file
                        </label>
                        <input
                            type="file"
                            name="file"
                            id="file"
                            style={{
                            display: "none"
                        }}></input>
                    </div>
                </div>
            </form>
        )
    }
}

{/*<form method="POST"  action="/test">

      </form>*/
}

export default UploadForm