import { BrowserRouter as Router, Switch } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProjectList from "./components/ProjectList";
import About from "./components/About";

function App() {
  return (
    <div>
      <Router>
        <Navbar />
        <Switch>
          <Router exact path="/">
            <ProjectList />
          </Router>
          <Router exact path="/about">
            <About />
          </Router>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
