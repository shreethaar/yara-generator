# yara-generator
Flask application for generating YARA rules, which are useful for malware detection and pattern matching.


To-do:
- [ ] Adding support for more yara features like wildcards
- [ ] Implement rule validation
- [ ] Including predefined templates
- [ x ]Export yar file feature
- [ ] Dark mode for sure


### Current Progess:
- **Completion:** 60%
- **Details:** 
  - Core functionalities for rule generation are implemented, including:
    - Parsing user inputs.
    - Formatting rule structures.
  - Remaining tasks include:
    - Validating user-provided data.
    - Adding more options for rule customization.


### Other Components
- Yet to be started:
  - `routes.py`: Define endpoints for handling user requests.
  - HTML templates: Design the interface for rule generation.
  - Static files: Enhance the visual appeal and interactivity of the app.

## Next Steps
1. Complete `yara_generator.py`.
2. Implement routing logic in `routes.py`.
3. Design UI templates in `templates/`.
4. Add test cases in the `tests/` directory. 
