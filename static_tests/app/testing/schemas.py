"""
Schemas for serialize LearningOutcome and Recommendation objects.
"""

from marshmallow import Schema, fields


class RecommendationSchema(Schema):
    name = fields.String(dump_only=True)
    task = fields.String(dump_only=True)


class LearningOutcomeSchema(Schema):
    name = fields.String(dump_only=True)
    score = fields.Integer(dump_only=True)
    recommendations = fields.Nested(RecommendationSchema, many=True)
