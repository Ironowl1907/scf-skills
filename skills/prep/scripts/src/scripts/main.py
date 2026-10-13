import yaml


def create_markdown_template(template_file):
    pass


def validate_dossier(dossier_file, tempte_file):
    pass


def main():
    with open("/home/ironowl/dev/scf-skills/skills/prep/scripts/brief-and-context.yaml", "r") as file:
        dossier_template = yaml.safe_load(file)


if __name__ == '__main__':
    main()
