import React, { Component } from 'react';

class PostsForm extends Component {
  constructor(props){
    super(props);
    this.state={
      title:'',
      body:''
    };
    this.onChange =this.onChange.bind(this);
  }
  onChange(e){
    this.setState({
      [e.target.name]:e.target.value
    });
  }
  render() {
    const {title,body} = this.state;
    const {onChange} = this;
    return (
      <div>
        <h4>new Post</h4>
        <form action="">
          <div>
            <label>title:</label>
            <input type="text" name="title" value={title} onChange={onChange}/>
          </div>
          <div>
            <label>body:</label>
            <input type="text" name="body" value={body} onChange={onChange}/>
          </div>
          <div><button type="submit">전송</button></div>
        </form>
      </div>
    );
  }
}

export default PostsForm;