import React from "react"
import PathConstants from "./constants"

const Game = React.lazy(() => import("../pages/Game"))
const About = React.lazy(() => import("../pages/About"))


const routes = [
    { path: PathConstants.GAME, element: <Game /> },
    { path: PathConstants.ABOUT, element: <About /> },
]
export default routes
