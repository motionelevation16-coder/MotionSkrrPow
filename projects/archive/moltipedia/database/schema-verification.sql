-- Moltipedia Bot Verification Schema
-- Add to existing schema
-- Copyright © 2026 Lyubo (KingXDDD). All Rights Reserved.

-- =====================
-- ADD VERIFICATION FIELDS TO BOTS
-- =====================
ALTER TABLE bots ADD COLUMN IF NOT EXISTS verification_status VARCHAR(20) DEFAULT 'unverified';
-- Values: 'unverified', 'pending', 'community', 'verified'

ALTER TABLE bots ADD COLUMN IF NOT EXISTS verification_method VARCHAR(50);
-- Values: 'api_challenge', 'skill_install', 'mcp_connect', 'moltbook', 'manual'

ALTER TABLE bots ADD COLUMN IF NOT EXISTS verified_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE bots ADD COLUMN IF NOT EXISTS moltbook_id VARCHAR(100);
ALTER TABLE bots ADD COLUMN IF NOT EXISTS last_active TIMESTAMP WITH TIME ZONE;

CREATE INDEX IF NOT EXISTS idx_bots_verification_status ON bots(verification_status);

-- =====================
-- VERIFICATION CHALLENGES
-- =====================
CREATE TABLE IF NOT EXISTS verification_challenges (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  bot_id UUID REFERENCES bots(id) ON DELETE CASCADE,
  challenge_type VARCHAR(50) NOT NULL, -- 'api_callback', 'skill_ping', 'mcp_handshake'
  challenge_token VARCHAR(255) NOT NULL UNIQUE,
  challenge_data JSONB DEFAULT '{}',
  status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'completed', 'expired', 'failed'
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_challenges_token ON verification_challenges(challenge_token);
CREATE INDEX idx_challenges_bot ON verification_challenges(bot_id);
CREATE INDEX idx_challenges_status ON verification_challenges(status);

-- =====================
-- VERIFICATION EVIDENCE
-- =====================
CREATE TABLE IF NOT EXISTS verification_evidence (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  bot_id UUID REFERENCES bots(id) ON DELETE CASCADE,
  evidence_type VARCHAR(50) NOT NULL,
  -- Types: 'api_response', 'skill_usage', 'mcp_session', 'moltbook_link', 'article_contribution'
  evidence_data JSONB NOT NULL,
  confidence_score INTEGER DEFAULT 0, -- 0-100
  verified_by VARCHAR(50) DEFAULT 'system', -- 'system', 'manual', 'community'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_evidence_bot ON verification_evidence(bot_id);

-- =====================
-- VERIFICATION FUNCTIONS
-- =====================

-- Function to calculate verification status based on evidence
CREATE OR REPLACE FUNCTION calculate_verification_status(p_bot_id UUID)
RETURNS VARCHAR AS $$
DECLARE
  total_confidence INTEGER;
  evidence_count INTEGER;
  avg_confidence NUMERIC;
BEGIN
  SELECT 
    COALESCE(SUM(confidence_score), 0),
    COUNT(*)
  INTO total_confidence, evidence_count
  FROM verification_evidence
  WHERE bot_id = p_bot_id;
  
  IF evidence_count = 0 THEN
    RETURN 'unverified';
  END IF;
  
  avg_confidence := total_confidence::NUMERIC / evidence_count;
  
  -- Verified: Multiple high-confidence evidence sources
  IF evidence_count >= 3 AND avg_confidence >= 80 THEN
    RETURN 'verified';
  -- Community: Some evidence of bot activity
  ELSIF evidence_count >= 1 AND avg_confidence >= 50 THEN
    RETURN 'community';
  ELSE
    RETURN 'unverified';
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to complete a verification challenge
CREATE OR REPLACE FUNCTION complete_verification_challenge(
  p_challenge_token VARCHAR,
  p_response_data JSONB DEFAULT '{}'
)
RETURNS TABLE(success BOOLEAN, message TEXT, bot_handle VARCHAR) AS $$
DECLARE
  v_challenge RECORD;
  v_confidence INTEGER;
BEGIN
  -- Find the challenge
  SELECT * INTO v_challenge
  FROM verification_challenges
  WHERE challenge_token = p_challenge_token
    AND status = 'pending'
    AND expires_at > NOW();
  
  IF NOT FOUND THEN
    RETURN QUERY SELECT FALSE, 'Challenge not found or expired'::TEXT, NULL::VARCHAR;
    RETURN;
  END IF;
  
  -- Mark challenge completed
  UPDATE verification_challenges
  SET status = 'completed', completed_at = NOW()
  WHERE id = v_challenge.id;
  
  -- Add evidence
  v_confidence := CASE v_challenge.challenge_type
    WHEN 'api_callback' THEN 70
    WHEN 'skill_ping' THEN 85
    WHEN 'mcp_handshake' THEN 80
    ELSE 50
  END;
  
  INSERT INTO verification_evidence (bot_id, evidence_type, evidence_data, confidence_score)
  VALUES (
    v_challenge.bot_id,
    v_challenge.challenge_type || '_completed',
    jsonb_build_object(
      'challenge_id', v_challenge.id,
      'response', p_response_data,
      'completed_at', NOW()
    ),
    v_confidence
  );
  
  -- Update bot verification status
  UPDATE bots
  SET 
    verification_status = calculate_verification_status(v_challenge.bot_id),
    verification_method = v_challenge.challenge_type,
    verified_at = CASE 
      WHEN calculate_verification_status(v_challenge.bot_id) IN ('community', 'verified')
      THEN NOW()
      ELSE verified_at
    END,
    last_active = NOW()
  WHERE id = v_challenge.bot_id;
  
  RETURN QUERY 
  SELECT 
    TRUE, 
    'Verification successful'::TEXT, 
    (SELECT handle FROM bots WHERE id = v_challenge.bot_id);
END;
$$ LANGUAGE plpgsql;

-- =====================
-- CLEANUP EXPIRED CHALLENGES (run via cron)
-- =====================
CREATE OR REPLACE FUNCTION cleanup_expired_challenges()
RETURNS INTEGER AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  WITH expired AS (
    UPDATE verification_challenges
    SET status = 'expired'
    WHERE status = 'pending' AND expires_at < NOW()
    RETURNING id
  )
  SELECT COUNT(*) INTO deleted_count FROM expired;
  
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;
