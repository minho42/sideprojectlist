import { useState } from "react";
import ProjectItem from "./ProjectItem";
import ProjectCounter from "./ProjectCounter";
import TagList from "./TagList";
import SortOptionList from "./SortOptionList";
import projectData from "../data.json";

const ProjectList = () => {
  const [data, setData] = useState(projectData);
  const [selectedTag, setSelectedTag] = useState("");

  const dataFilteredByTag = () => {
    if (!selectedTag | (selectedTag === "all")) {
      return data;
    }
    return data.filter((item) => {
      return item.tags.includes(selectedTag);
    });
  };

  return (
    <div className="mx-1">
      <div className="flex items-center pt-4 pb-2 mx-4 justify-start">
        <div className="flex items-center text-2xl font-semibold">
          <div>
            <TagList data={data} selectedTag={selectedTag} setSelectedTag={setSelectedTag} />
            <ProjectCounter
              count={selectedTag ? dataFilteredByTag().length : data.length}
              selectedTag={selectedTag}
              setSelectedTag={setSelectedTag}
            />
            {!selectedTag ? <SortOptionList data={data} setData={setData} /> : ""}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap">
        {dataFilteredByTag().map((item) => {
          return (
            <ProjectItem
              key={item.id}
              item={item}
              selectedTag={selectedTag}
              setSelectedTag={setSelectedTag}
            />
          );
        })}
      </div>
    </div>
  );
};

export default ProjectList;
