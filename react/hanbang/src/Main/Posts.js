import React, { Component } from 'react';

class Posts extends Component {
    /* 컴포넌트 생성시 */
    /* 생명주기순서 : constructor(생성자) -> componentWillMount -> render */

    constructor(props) {
        super(props);
        this.state = {
            posts: []
        }
    }
    componentWillMount() {
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then(res => res.json())
            .then(data => this.setState({
                posts: data
            }));
    }
    render() {
        const { posts } = this.state;
        const postsList = posts.map((post) => (
            <div key={post.id} id={post.id}>
                <span>count 1</span>
                <h4>{post.title}</h4>
                <h4>{post.body}</h4>
            </div>
        ));
        return (
            <div>
                {postsList}
            </div>
        );
    }
}
export default Posts;