from flask import jsonify, request
from flask_restful import Api, Resource

from ..exchanges.multi_exchange_manager import MultiExchangeManager
from ..ai.advanced_adaptation import AdvancedAdaptationAI

api = Api()


class BalanceAPI(Resource):
    def get(self):
        exchange_manager = MultiExchangeManager()
        return jsonify(exchange_manager.get_aggregated_balance())


class AIRecommendationAPI(Resource):
    def get(self):
        exchange_manager = MultiExchangeManager()
        ai = AdvancedAdaptationAI()
        balances = exchange_manager.get_aggregated_balance()
        # For scaffold, use a dummy volatility value
        current_volatility = request.args.get('volatility', 0.1)
        recommendation = ai.dynamic_strategy_adjustment(balances, float(current_volatility))
        return jsonify(recommendation)


api.add_resource(BalanceAPI, '/api/mobile/balance')
api.add_resource(AIRecommendationAPI, '/api/mobile/ai-recommendations')
