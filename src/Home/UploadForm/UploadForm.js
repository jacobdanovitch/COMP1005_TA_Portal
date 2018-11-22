import React from 'react'

class UploadForm extends React.Component {
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