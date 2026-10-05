# SCF skills

## Design choices
- All skills are designed to be invoked manually by the user only. For that, there's the metadata field `disable-model-invocation` and a statement at the end of each skill's `description` field.
- All skills are also designed to be *model agnostic*. They must follow the Agent Skills spec to the letter.

## Attribution
*Grilling protocol adapted from Matt Pocock's `grilling` skill (github.com/mattpocock/skills).*
