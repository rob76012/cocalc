import * as React from "react";

const { Space, Icon } = require("../../r_misc");
const { Button } = require("react-bootstrap");

export function PublicButton({ on_click }) {
  return (
    <span>
      <Space />
      <Button bsStyle="info" bsSize="xsmall" onClick={on_click}>
        <Icon name="bullhorn" /> <span className="hidden-xs">Public</span>
      </Button>
    </span>
  );
}
