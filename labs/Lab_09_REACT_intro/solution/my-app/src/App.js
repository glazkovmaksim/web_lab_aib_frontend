import Counter from "./component/Task1/Task1";
import Post from "./component/Task2/Task2";
import PostFour from "./component/Task4/Task3";
function App() {
  return (
    <div className="App">
      {/* Первое задание */}
      <Counter />
      {/* Второе задание и третье вместе */}
       <Post /> 
      {/* Четвертое задание */}
      <PostFour />
    </div>
  );
}

export default App;