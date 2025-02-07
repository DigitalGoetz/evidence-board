import { useState } from "react";
import Home from "./pages/Home.jsx";
import ItemView from "./components/ItemView.jsx";
import { RuxGlobalStatusBar, RuxTab, RuxTabPanel, RuxTabPanels, RuxTabs } from "@astrouxds/react";

function NavigationTabs({selectedTab, onTabSelect}) {

  const handleTabClick = (event) => {
    onTabSelect(event.target.value);
  };

  return (
    <RuxTabs>
      <RuxTab key="home" value="/" onClick={handleTabClick} selected={selectedTab ==="/"}>Home</RuxTab>
      <RuxTab key="tags" value="/tags" onClick={handleTabClick} selected={selectedTab === "/tags"}>Tags</RuxTab>
      <RuxTab key="groups" value="/groups" onClick={handleTabClick} selected={selectedTab === "/groups"}>Groups</RuxTab>
      <RuxTab key="people" value="/people" onClick={handleTabClick} selected={selectedTab === "/people"}>People</RuxTab>
      <RuxTab key="places" value="/places" onClick={handleTabClick} selected={selectedTab === "/places"}>Places</RuxTab>
      <RuxTab key="locations" value="/locations" onClick={handleTabClick} selected={selectedTab === "/locations"}>Locations</RuxTab>
    </RuxTabs>
  );
}

function App() {
  const [selectedTab, setSelectedTab] = useState("/");

  const renderPanels = () => {
    switch(selectedTab){
      case "/":
        return <RuxTabPanel key="home" selected={true}><Home /></RuxTabPanel>
      case "/tags":
        return <RuxTabPanel key="tags" selected={true}><ItemView api="tags" /></RuxTabPanel>
      case "/groups":
        return <RuxTabPanel key="groups" selected={true}><ItemView api="groups" /></RuxTabPanel>
      case "/people":
        return <RuxTabPanel key="people" selected={true}><ItemView api="people" /></RuxTabPanel>
      case "/places":
        return <RuxTabPanel key="places" selected={true}><ItemView api="places" /></RuxTabPanel>
      case "/locations":
        return <RuxTabPanel key="locations" selected={true}><ItemView api="locations" /></RuxTabPanel>
    }
  }

  return (
    <>
      <RuxGlobalStatusBar
        includeIcon
        menuIcon="search"
        appName="Evidence Board"
      >
        <NavigationTabs selectedTab={selectedTab} onTabSelect={setSelectedTab} />
      </RuxGlobalStatusBar>

      <RuxTabPanels>
        {renderPanels()}
      </RuxTabPanels>
    </>
  );
}

export default App;
