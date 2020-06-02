import React, { Fragment } from 'react';


class ChartArea extends React.Component{
    constructor(props){
        super(props);   
    }


    render(){
        var guName = this.props.name;
        var dongNum = this.props.dongNum;


        return( 
            <div>
                {guName}
                {dongNum}



            </div>
        
        )
    }
}

export default ChartArea;