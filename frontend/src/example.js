import React, { Component } from 'react';
// import logo from './logo.svg';
//import './App.css';

// EXAMPLE REACT CODE

class App extends Component {
  // state
  constructor(props) {

    super(props)

    this.state = {
      board = Array(9).fill(null)
    }

  }

  // somehow change the state
  handleClick(index) {

    let newBoard = this.state.board

    newBoard[index] = "X"

    this.setState({
      board: newBoard

      player:
    })

    console.log(this.state.board)

    console.log(index)
  }

  render() {

    const Box = this.state.board.map(
      (box,index) =>
      <div className="box"
        key={index}
        onClick={() => this.handleClick(index)}>
        {box}
      </div>)

    return (
      {Box}
    );
  }
}

export default App;
