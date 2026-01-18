version: 2

models:
  - name: fct_image_detections
    description: "Fact table of image detections with classifications, joined to messages."
    columns:
      - name: message_id
        tests:
          - not_null
          - unique
      - name: confidence_score
        tests:
          - not_null
      - name: image_category
        tests:
          - not_null
          - accepted_values:
              values: ['promotional', 'product_display', 'lifestyle', 'other']
